"""
Copyright 2023 [PT BOOKBOT INDONESIA](https://bookbot.id/)

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import json
import os

import numpy as np
import onnxruntime

from g2p_id.onnx_utils import WrapInferenceSession

model_path = os.path.join(os.path.dirname(__file__), "models", "bert")


class BERT:
    """Phoneme-level BERT model for predicting the correct phoneme for the letter `e`.
    Trained with [Keras](https://keras.io/examples/nlp/masked_language_modeling/),
    and exported to ONNX. ONNX Runtime engine used during inference.
    """

    def __init__(self):
        bert_model_path = os.path.join(model_path, "bert_mlm.onnx")
        token2id = os.path.join(model_path, "token2id.json")
        config_path = os.path.join(model_path, "config.json")
        self.model = WrapInferenceSession(bert_model_path, providers=onnxruntime.get_available_providers())
        with open(config_path, encoding="utf-8") as file:
            self.config = json.load(file)
        with open(token2id, encoding="utf-8") as file:
            self.token2id = json.load(file)
        self.id2token = {v: k for k, v in self.token2id.items()}

    def predict(self, text: str) -> str:
        """Performs BERT inference, predicting the correct phoneme for the letter `e`.

        Args:
            text (str): Word to predict from.

        Returns:
            str: Word after prediction.
        """
        # `x` is currently OOV, we replace with
        text = text.replace("x", "ks")
        # mask `e`'s
        text = " ".join([c if c != "e" else "[mask]" for c in text])

        # tokenize and pad to max length
        tokens = [self.token2id[c] for c in text.split()]
        padding = [self.token2id[self.config["pad_token"]] for _ in range(self.config["max_seq_length"] - len(tokens))]
        tokens = tokens + padding

        input_ids = np.array([tokens], dtype="int64")
        inputs = {"input_1": input_ids}
        prediction = self.model.run(None, inputs)

        # find masked idx token
        mask_token_id = self.token2id[self.config["mask_token"]]
        masked_index = np.where(input_ids == mask_token_id)[1]

        # get prediction at masked indices
        mask_prediction = prediction[0][0][masked_index]
        predicted_ids = np.argmax(mask_prediction, axis=1)

        # replace mask with predicted token
        for i, idx in enumerate(masked_index):
            tokens[idx] = predicted_ids[i]

        return "".join([self.id2token[t] for t in tokens if t != 0])
