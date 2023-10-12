class ErrorMessage:

    BAD_REQUEST = "field missing"
    UNAUTHORIZED = "unauthorized"
    NOT_FOUND = "not found"
    INTERNAL_ERROR = "internal error"
    ALREADY_EXISTS = "already exists"
    DB_UPDATE= "document update failed"
    DB_INSERT = "document insert failed"
    DB_CONNECTION = "db connection error"
    DB_GET_CONNECTION_POOL = "db get connection from pool error"
    DB_CLOSE_CURSOR_CONNECTION = "db close cursor error"
    DB_PUT_CONNECTION_TO_POOL = "db put connection to pool error"
    DB_SELECT = "db select error"
    DB_DELETE = "document delete failed"

    FILE = "File too large"
    ROLE = "User role is not consistent with the request"
