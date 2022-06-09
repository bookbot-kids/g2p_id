"""
Copyright 2022 [PT BOOKBOT INDONESIA](https://bookbot.id/)

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

import os
import json
import numpy as np
import onnxruntime as ort

model_path = os.path.join(os.path.dirname(__file__), "models", "lstm")


class LSTM:
    def __init__(self):
        encoder_model_path = os.path.join(model_path, "encoder_model.onnx")
        decoder_model_path = os.path.join(model_path, "decoder_model.onnx")
        g2id_path = os.path.join(model_path, "g2id.json")
        p2id_path = os.path.join(model_path, "p2id.json")
        config_path = os.path.join(model_path, "config.json")
        self.encoder = ort.InferenceSession(encoder_model_path)
        self.decoder = ort.InferenceSession(decoder_model_path)
        self.g2id = json.load(open(g2id_path, encoding="utf-8"))
        self.p2id = json.load(open(p2id_path, encoding="utf-8"))
        self.id2p = {v: k for k, v in self.p2id.items()}
        self.config = json.load(open(config_path, encoding="utf-8"))

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

        for t, char in enumerate(text):
            input_seq[0, t, self.g2id[char]] = 1.0
        input_seq[0, t + 1 :, self.g2id[self.config["pad_token"]]] = 1.0

        encoder_inputs = {"input_1": input_seq}
        states_value = self.encoder.run(None, encoder_inputs)

        target_seq = np.zeros(
            (1, 1, self.config["num_decoder_tokens"]), dtype="float32"
        )
        target_seq[0, 0, self.p2id[self.config["bos_token"]]] = 1.0

        stop_condition = False
        decoded_sentence = ""
        while not stop_condition:
            decoder_inputs = {
                "input_2": target_seq,
                "input_3": states_value[0],
                "input_4": states_value[1],
            }
            output_tokens, h, c = self.decoder.run(None, decoder_inputs)

            sampled_token_index = np.argmax(output_tokens[0, -1, :])
            sampled_char = self.id2p[sampled_token_index]
            decoded_sentence += sampled_char

            if (
                sampled_char == self.config["eos_token"]
                or len(decoded_sentence) > self.config["max_decoder_seq_length"]
            ):
                stop_condition = True

            target_seq = np.zeros(
                (1, 1, self.config["num_decoder_tokens"]), dtype="float32"
            )
            target_seq[0, 0, sampled_token_index] = 1.0

            states_value = [h, c]

        return decoded_sentence.replace(self.config["eos_token"], "")


def main():
    texts = ["mengembangkannya", "merdeka", "pecel", "lele"]
    lstm = LSTM()
    for text in texts:
        print(lstm.predict(text))


if __name__ == "__main__":
    main()
