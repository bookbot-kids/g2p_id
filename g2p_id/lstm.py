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

model_path = os.path.join(os.path.dirname(__file__), "models", "lstm")


class LSTM:
    """Phoneme-level LSTM model for sequence-to-sequence phonemization.
    Trained with [Keras](https://keras.io/examples/nlp/lstm_seq2seq/),
    and exported to ONNX. ONNX Runtime engine used during inference.
    """

    def __init__(self):
        encoder_model_path = os.path.join(model_path, "encoder_model.onnx")
        decoder_model_path = os.path.join(model_path, "decoder_model.onnx")
        g2id_path = os.path.join(model_path, "g2id.json")
        p2id_path = os.path.join(model_path, "p2id.json")
        config_path = os.path.join(model_path, "config.json")
        self.encoder = WrapInferenceSession(
            encoder_model_path,
            providers=onnxruntime.get_available_providers(),
        )
        self.decoder = WrapInferenceSession(
            decoder_model_path,
            providers=onnxruntime.get_available_providers(),
        )
        with open(g2id_path, encoding="utf-8") as file:
            self.g2id = json.load(file)
        with open(p2id_path, encoding="utf-8") as file:
            self.p2id = json.load(file)
        self.id2p = {v: k for k, v in self.p2id.items()}
        with open(config_path, encoding="utf-8") as file:
            self.config = json.load(file)

    def predict(self, text: str) -> str:
        """Performs LSTM inference, predicting phonemes of a given word.

        Args:
            text (str): Word to convert to phonemes.

        Returns:
            str: Word in phonemes.
        """
        input_seq = np.zeros(
            (
                1,
                self.config["max_encoder_seq_length"],
                self.config["num_encoder_tokens"],
            ),
            dtype="float32",
        )

        for idx, char in enumerate(text):
            input_seq[0, idx, self.g2id[char]] = 1.0
        input_seq[0, len(text) :, self.g2id[self.config["pad_token"]]] = 1.0

        encoder_inputs = {"input_1": input_seq}
        states_value = self.encoder.run(None, encoder_inputs)

        target_seq = np.zeros((1, 1, self.config["num_decoder_tokens"]), dtype="float32")
        target_seq[0, 0, self.p2id[self.config["bos_token"]]] = 1.0

        stop_condition = False
        decoded_sentence = ""
        while not stop_condition:
            decoder_inputs = {
                "input_2": target_seq,
                "input_3": states_value[0],
                "input_4": states_value[1],
            }
            output_tokens, state_memory, state_carry = self.decoder.run(None, decoder_inputs)

            sampled_token_index = np.argmax(output_tokens[0, -1, :])
            sampled_char = self.id2p[sampled_token_index]
            decoded_sentence += sampled_char

            if (
                sampled_char == self.config["eos_token"]
                or len(decoded_sentence) > self.config["max_decoder_seq_length"]
            ):
                stop_condition = True

            target_seq = np.zeros((1, 1, self.config["num_decoder_tokens"]), dtype="float32")
            target_seq[0, 0, sampled_token_index] = 1.0

            states_value = [state_memory, state_carry]

        return decoded_sentence.replace(self.config["eos_token"], "")
