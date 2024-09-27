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

import onnxruntime as ort


class WrapInferenceSession:
    """Wrapper class for serializing ONNX InferenceSession objects.
    Based on: https://github.com/microsoft/onnxruntime/pull/800#issuecomment-844326099
    """

    def __init__(self, onnx_bytes, sess_options=None, providers=None):
        self.sess = ort.InferenceSession(onnx_bytes, sess_options=sess_options, providers=providers)
        self.onnx_bytes = onnx_bytes
        self.providers = providers

    def run(self, *args):
        """Wrapper for ONNX InferenceSession run method.

        Returns:
            Any: Inference result.
        """
        return self.sess.run(*args)

    def __getstate__(self):
        return {"onnx_bytes": self.onnx_bytes}

    def __setstate__(self, values):
        self.onnx_bytes = values["onnx_bytes"]
        self.providers = values.get("providers", None)
        self.sess = ort.InferenceSession(self.onnx_bytes, self.providers)
