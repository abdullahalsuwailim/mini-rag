from enum import Enum 

class ResponseSignal(Enum):
    FILE_TYPE_NOT_ALLOWED = "this file type is not allowed"
    FILE_TOO_LARGE = "this file is too large"
    FILE_UPLOAD_SUCCESS = "success"
    FILE_UPLOAD_FAILED = "file upload failed"