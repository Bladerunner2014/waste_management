class InfoMessage:
    ACCESS_REQUEST = "access_request"
    ACCESS_RESPONSE = "access_response"

    AUTHORIZED_ACCESS = "authorized"
    UNAUTHORIZED_ACCESS = "unauthorized"
    DB_FIND = "document found successfully"
    DB_QUERY = "db query"
    NOT_FOUND = "did not found found any document"
    GET_REQUEST = "user {username} sent a get request: {imsi}"
    DB_INSERT = "document inserted successfully"
    POST_REQUEST = "user {username} sent a post request: {document}"
    DB_UPDATED = "database updated successfully"
    PUT_REQUEST = "user {username} sent a put request: {document}"
    DELETE_REQUEST = "user {username} sent a delete request: {document}"
    DB_DELETE = "document delete successfully"
    USER_CREATED = "user created successfully"
    EMAIL = "email sent"
