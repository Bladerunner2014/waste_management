from typing import Annotated
from manager.handler import RequestManager, SignUp, FormManager
from fastapi import FastAPI, Body, UploadFile, File
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
def get_form_structure(form_id, current_user: Annotated[UserSignIn, Depends(get_current_active_user)] = None,
                       ):
    condition = {'form_id': form_id}

    logger.info(InfoMessage.GET_REQUEST.format(username=current_user.username, form_name=form_id))

    mg = RequestManager(config['FORM_STRUCTURE_DB_COLLECTION_NAME'])
    res = mg.find(condition)
    return res.generate_response()


@app.delete("/del_struct/{form_id}", tags=["form_struct_crud"])
def delete_crud(form_id,
                current_user: Annotated[UserSignIn, Depends(get_current_active_user)] = None):
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ErrorMessage.ROLE)
    condition = {"form_id": form_id}
    logger.info(InfoMessage.DELETE_REQUEST.format(username=current_user.username, document=form_id))
    mg = RequestManager(config['FORM_STRUCTURE_DB_COLLECTION_NAME'])
    res = mg.delete(condition)
    return res.generate_response()


@app.post("/form_upload", tags=["form_struct_crud"])
async def create_upload_file(file: UploadFile = File(...),
                             current_user: Annotated[UserSignIn, Depends(get_current_active_user)] = None,
                             ):
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ErrorMessage.ROLE)

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
def post(current_user: Annotated[UserSignIn, Depends(get_current_active_user)] = None,
         doc: Annotated[dict | None, Body(examples=[model_config], description="Document")] = None):
    logger.info(InfoMessage.POST_REQUEST.format(username=current_user.username, document=doc))

    mg = RequestManager(config['FORMS_COLLECTION_NAME'])
    # res = mg.check_action(dict(doc))
    res = mg.insert(doc)
    return res.generate_response()


@app.get("/get_form/{form_id}", tags=["form_crud"])
def get_form(form_id, current_user: Annotated[UserSignIn, Depends(get_current_active_user)] = None,
             ):
    condition = {'form_id': form_id}

    logger.info(InfoMessage.GET_REQUEST.format(username=current_user.username, form_name=form_id))

    mg = RequestManager(config['FORMS_COLLECTION_NAME'])
    res = mg.find(condition)
    return res.generate_response()


@app.delete("/del_form/{form_id}", tags=["form_crud"])
def delete_crud(form_id,
                current_user: Annotated[UserSignIn, Depends(get_current_active_user)] = None):
    # if current_user.role != "admin":
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ErrorMessage.ROLE)
    condition = {"form_id": form_id}
    logger.info(InfoMessage.DELETE_REQUEST.format(username=current_user.username, document=form_id))
    mg = RequestManager(config['FORMS_COLLECTION_NAME'])
    res = mg.delete(condition)
    return res.generate_response()


@app.put("/update_form/{form_id}", tags=["form_crud"])
def put_crud(form_id,
             doc: Annotated[dict | None, Body(examples=[model_config], description="Document")] = None,
             current_user: Annotated[UserSignIn, Depends(get_current_active_user)] = None):
    # if current_user.role != "one":
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ErrorMessage.ROLE)

    logger.info(InfoMessage.PUT_REQUEST.format(username=current_user.username, document=doc))
    mg = RequestManager(config['FORMS_COLLECTION_NAME'])
    res = mg.update({"form_id":form_id}, dict(doc))
    return res.generate_response()


@app.post("/token", tags=["auth"], response_model=Token)
async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = authenticate_user(username=form_data.username, password=form_data.password)
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


@app.post("/sign_up", tags=["auth"])
async def sign_up(
        user_info: Annotated[UserSignIn | None, Body(examples=[user_sign_in], description="Sign up")] = None):
    logger.info(user_info)

    mg = SignUp()
    res = mg.sign_up(dict(user_info))

    return res.generate_response()


log.setup_logger()
