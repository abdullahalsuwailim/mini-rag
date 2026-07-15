from enum import Enum 

class ResponseSignal(Enum):
    FILE_TYPE_NOT_ALLOWED = "this_file_type_is_not_allowed"
    FILE_TOO_LARGE = "this_file_is_too_large"
    FILE_UPLOAD_SUCCESS = "success"
    FILE_UPLOAD_FAILED = "file_upload_failed"
    PROCESSING_SUCCESS = "success"
    PROCESSING_FAILED = "processing_failed"
    NO_FILE_ERROR = "no_file_found"
    FILE_ID_ERROR = "no_file_found_with_this_id"
    PROJECT_NOT_FOUND_ERROR = "project_not_found"
    INSERT_INTO_VECTORDB_ERROR = "insert_into_vectordb_error"
    INSERT_INTO_VECTORDB_SUCCESS = "insert_into_vectordb_success"
    VECTORDB_COLLECTION_RETRIEVED = "vectordb_collection_retrieved"
    VECTORDB_SEARCH_SUCCESS = "vectordb_search_success"
    VECTORDB_SEARCH_ERROR = "vectordb_search_error"