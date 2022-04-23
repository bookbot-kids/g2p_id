import os
import json
import numpy as np
import onnxruntime as ort

model_path = os.path.join(os.path.dirname(__file__), "models", "bert")


class BERT:
    def __init__(self):
        bert_model_path = os.path.join(model_path, "bert_mlm.onnx")
        token2id = os.path.join(model_path, "token2id.json")
        config_path = os.path.join(model_path, "config.json")
        self.model = ort.InferenceSession(bert_model_path)
        self.token2id = json.load(open(token2id, encoding="utf-8"))
        self.id2token = {v: k for k, v in self.token2id.items()}
        self.config = json.load(open(config_path, encoding="utf-8"))

    def predict(self, text: str) -> str:
        """Performs BERT inference, predicting the correct phoneme for the letter `e`.

        Parameters
        ----------
        text : str
            Word to predict from.

        Returns
        -------
        str
            Word after prediction.
        """
        # mask `e`'s
        text = " ".join([c if c != "e" else "[mask]" for c in text])

        # tokenize and pad to max length
        tokens = [self.token2id[c] for c in text.split()]
        padding = [
            self.token2id[self.config["pad_token"]]
            for _ in range(self.config["max_seq_length"] - len(tokens))
        ]
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


def main():
    texts = ["mengembangkannya", "merdeka", "pecel", "lele"]
    bert = BERT()
    for text in texts:
        print(bert.predict(text))


if __name__ == "__main__":
    main()
