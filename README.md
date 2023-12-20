![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-black?style=for-the-badge&logo=JSON%20web%20tokens)
![Docker](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white)
![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white)
![Swagger](https://img.shields.io/badge/-Swagger-%23Clojure?style=for-the-badge&logo=swagger&logoColor=white)
![MinIO Badge](https://img.shields.io/badge/MinIO-C72E49?logo=minio&logoColor=fff&style=flat-square)

## How does it works?
## Run with docker:
Run the following command in the project root:
```bash
# clone the project
git clone https://github.com/mohammad-mahdi-rajabi/waste-management.git

# or usin ssh
git clone git@github.com:mohammad-mahdi-rajabi/waste-management.git

cd waste-management

# run project with docker and docker-compose
docker-compose up -d
```
This command will build container image and run it on 80000 port. you can change the listening port in docker-compose file by changing the 8008 in ports section:
```bash
version: '3'

services:

  wst-mng:
    build: .
#    command: gunicorn core.wsgi:application --bind 0.0.0.0:8000
    expose:
      - "8000"
    depends_on:
          - postgres
  postgres:
    image: postgres
    ports:
      - "5432"
    volumes:
      - db:/var/lib/postgresql/data

    environment:
      POSTGRES_USER: 'postgres'
      POSTGRES_PASSWORD: '1234'
      POSTGRES_DB: form
#  nginx:
#    build: ./nginx
#    restart: always
#    ports:
#      - "1337:80"
#    depends_on:
#        - wst-mng
volumes:
  db:
```


## Run bare metal on your machine:

## API documents are available in swagger:
After running the app, open the following address in your browser:
```bash
http://127.0.0.1:8000/api/schema/docs/
```
**Note:**

# License
[![Licence](https://img.shields.io/github/license/Ileriayo/markdown-badges?style=for-the-badge)](./LICENSE)
