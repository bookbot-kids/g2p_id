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
        return self.sess.run(*args)

    def __getstate__(self):
        return {"onnx_bytes": self.onnx_bytes}

    def __setstate__(self, values):
        self.onnx_bytes = values["onnx_bytes"]
        self.providers = values["providers"]
        self.sess = ort.InferenceSession(self.onnx_bytes, self.providers)
