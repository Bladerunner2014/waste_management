from typing import Annotated
from manager.handler import RequestManager, FormManager
from fastapi import FastAPI, Body, UploadFile, File, Request
import logging
from constants.info_message import InfoMessage
from constants.error_message import ErrorMessage
from models.models import Token, UserSignIn, model_config, UserSignIn, user_sign_in
from log import log
from security.details import *
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from fastapi.middleware.cors import CORSMiddleware
from security.details import get_user
from dao.mongodao import WasteManagementDao
# from security import utils
from random import randbytes
import hashlib
from mail.mailservice import send_mail, expire_verification_code
from threading import Thread
from security.details import get_password_hash

tags_metadata = [
    {
        "name": "form_crud",
        "description": "With this endpoint you can POST/PUT/GET/DELETE documents in mongoDB.",
    },
    {
        "name": "auth",
        "description": "This endpoint handle the authentication of users.",

    },
    {
        "name": "form_struct_crud",
        "description": "To CRUD forms structs in database (only admin can access these endpoints).",

    }
]
app = FastAPI(openapi_tags=tags_metadata)
origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
config = dotenv_values(".env")
logger = logging.getLogger(__name__)


@app.get("/get_struct/{form_id}", tags=["form_struct_crud"])
def get_form_structure(form_id
                       ):
    condition = {'form_id': form_id}

    # logger.info(InfoMessage.GET_REQUEST.format(username=current_user.username, form_name=form_id))

    mg = RequestManager(config['FORM_STRUCTURE_DB_COLLECTION_NAME'])
    res = mg.find(condition)
    return res.generate_response()


@app.delete("/del_struct/{form_id}", tags=["form_struct_crud"])
def delete_crud(form_id):
    # if current_user.role != "admin":
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ErrorMessage.ROLE)
    condition = {"form_id": form_id}
    # logger.info(InfoMessage.DELETE_REQUEST.format(username=current_user.username, document=form_id))
    mg = RequestManager(config['FORM_STRUCTURE_DB_COLLECTION_NAME'])
    res = mg.delete(condition)
    return res.generate_response()


@app.post("/form_upload", tags=["form_struct_crud"])
async def create_upload_file(file: UploadFile = File(...),

                             ):
    # if current_user.role != "admin":
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ErrorMessage.ROLE)

    # Get the file size (in bytes)
    file.file.seek(0, 2)
    file_size = file.file.tell()

    # move the cursor back to the beginning
    await file.seek(0)
    if file_size > 2 * 1024 * 1024:
        # more than 2 MB
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="File too large")

    # check the content type (MIME type)
    content_type = file.content_type
    if content_type not in ["text/csv"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid file type")
    w_file = file.file.read()
    with open("new_form.csv", "wb") as writer:
        writer.write(w_file)

    mg = FormManager()
    res = mg.csv_processor()
    return res.generate_response()


@app.post("/post_form/", tags=["form_crud"], response_model=dict)
def post(
         doc: Annotated[dict | None, Body(examples=[model_config], description="Document")] = None):
    # logger.info(InfoMessage.POST_REQUEST.format(username=current_user.username, document=doc))

    mg = RequestManager(config['FORMS_COLLECTION_NAME'])
    # res = mg.check_action(dict(doc))
    res = mg.insert(doc)
    return res.generate_response()


@app.get("/get_form/{form_id}", tags=["form_crud"])
def get_form(form_id
             ):
    condition = {'form_id': form_id}

    # logger.info(InfoMessage.GET_REQUEST.format(username=current_user.username, form_name=form_id))

    mg = RequestManager(config['FORMS_COLLECTION_NAME'])
    res = mg.find(condition)
    return res.generate_response()


@app.delete("/del_form/{form_id}", tags=["form_crud"])
def delete_crud(form_id,
                ):
    # if current_user.role != "admin":
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ErrorMessage.ROLE)
    condition = {"form_id": form_id}
    # logger.info(InfoMessage.DELETE_REQUEST.format(username=current_user.username, document=form_id))
    mg = RequestManager(config['FORMS_COLLECTION_NAME'])
    res = mg.delete(condition)
    return res.generate_response()


@app.put("/update_form/{form_id}", tags=["form_crud"])
def put_crud(form_id,
             doc: Annotated[dict | None, Body(examples=[model_config], description="Document")] = None,
             ):
    # if current_user.role != "one":
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ErrorMessage.ROLE)

    # logger.info(InfoMessage.PUT_REQUEST.format(username=current_user.username, document=doc))
    mg = RequestManager(config['FORMS_COLLECTION_NAME'])
    res = mg.update({"form_id": form_id}, dict(doc))
    return res.generate_response()


@app.post("/token", tags=["auth"], response_model=Token)
async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = authenticate_user(username=form_data.username, password=form_data.password)
    print(user)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=int(config["ACCESS_TOKEN_EXPIRE_MINUTES"]))
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


@app.post('/register', status_code=status.HTTP_201_CREATED, tags=["auth"])
async def create_user(payload: UserSignIn, request: Request):
    # Check if user already exist
    dao = WasteManagementDao(config["USER_COLLECTION_NAME"], config["DB_NAME"])
    user = dao.find({'email': payload.email.lower()})
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail='Account already exist')
    # Compare password and passwordConfirm
    if payload.password != payload.passwordConfirm:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='Passwords do not match')
    #  Hash the password
    payload.password = get_password_hash(payload.password)
    # del payload.passwordConfirm
    payload.role = 'admin'
    payload.verified = False
    payload.email = payload.email.lower()
    payload.created_at = datetime.utcnow()
    payload.updated_at = payload.created_at

    result = dao.insert_one(dict(payload))
    new_user = dao.find({'email': payload.email.lower()})
    try:
        token = randbytes(6)
        print(token.hex())
        hashedCode = hashlib.sha256()
        hashedCode.update(token)
        verification_code = hashedCode.hexdigest()
        dao.db.find_one_and_update({'email': payload.email.lower()}, {
            "$set": {"verification_code": verification_code, "updated_at": datetime.utcnow()}})

        await send_mail("verification_code: {}".format(token.hex()), payload.email.lower())
    except Exception as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail='There was an error sending email')
    thread = Thread(target=expire_verification_code, args=({'email': payload.email.lower()}, {
        "$set": {"verification_code": None, "updated_at": datetime.utcnow()}}))
    thread.start()
    return {'status': 'success', 'message': 'Verification token successfully sent to your email'}


@app.get('/verifyemail/{token}', tags=["auth"])
def verify_me(token):
    hashedCode = hashlib.sha256()
    hashedCode.update(bytes.fromhex(token))
    verification_code = hashedCode.hexdigest()
    dao = WasteManagementDao(config["USER_COLLECTION_NAME"], config["DB_NAME"])
    result = dao.db.find_one_and_update({"verification_code": verification_code}, {
        "$set": {"verification_code": None, "verified": True, "updated_at": datetime.utcnow()}}, new=True)

    if not result:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail='Invalid verification code or account already verified')
    return {
        "status": "success",
        "message": "Account verified successfully"
    }


log.setup_logger()
