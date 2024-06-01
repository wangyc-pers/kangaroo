
class SoftDeleteNotSupported(Exception):
    def __init__(self, model_name):
        self.message = f"Soft delete is not supported for {model_name}"
        super().__init__(self.message)
