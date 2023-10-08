![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![MongoDB](https://img.shields.io/badge/MongoDB-%234ea94b.svg?style=for-the-badge&logo=mongodb&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-black?style=for-the-badge&logo=JSON%20web%20tokens)
![Docker](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white)
![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white)
![Swagger](https://img.shields.io/badge/-Swagger-%23Clojure?style=for-the-badge&logo=swagger&logoColor=white)


# Costum MongoDB WebUI with authentication by bladerunner
A UI powered by **FastAPI**. You can manage MongoDB database via CRUD endpoints.

## Endpoints
1. MongoDB CRUD 🏠
2. Authentication 💻

## How does it works?
## Run with docker:
Run the following command in the project root:
```bash
# clone the project
git clone [https://git@git.siz-tel.com:2222/bladerunner/MongoDB_WebUI_UPDATED.git](https://github.com/Bladerunner2014/waste_management.git)

# or usin ssh
git clone git@github.com:Bladerunner2014/waste_management.git

cd MongoDB_WebUI_UPDATED

# run project with docker and docker-compose
docker-compose up -d
```
This command will build container image and run it on 8008 port. you can change the listening port in docker-compose file by changing the 8008 in ports section:
```bash
version: '3'

services:
  web:
    build: .
    command: uvicorn main:app --host 0.0.0.0
    volumes:
      - .:/infra
    ports:
      - "8008:8000"
```


## Run bare metal on your machine:
Run the following command in the project root:
```bash
uvicorn main:app --reload
```
**Note:**
Dont use --reload in production!


## API documents are available in swagger:
After running the app, open the following address in your browser:
```bash
http://127.0.0.1:8000/docs
```
**Note:**
Change the host and port with your costum host and port. You should see the following page containing the API documents:
<p align="center">
<img src='./swagger.png' style="border: white;border-radius: 2pc;" alt='trojan horse'/>
</p>


# License
[![Licence](https://img.shields.io/github/license/Ileriayo/markdown-badges?style=for-the-badge)](./LICENSE)
