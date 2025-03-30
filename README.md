# audio_storage


This is a simple FastAPI app which imitates audio storage.

The user can upload audio files and give them name in the API.

User can authorize through Yandex.

Available endpoints:

GET /login/yandex - redirects to yandex autorization page

GET /pages/index - returns form for file submission

POST /api/v1/files/upload - sends audio files to server (.mp3, .wav, .ogg, .flac)

  -H "Content-Type: multipart/form-data" 
  
  -F "file_name=myfile"
  
  -F "file=<file_path>"

GET /api/v1/files/{email} - returns file names and paths for user with provided email

Endpoints for superuser:

GET /api/v1/users - returns all users

POST /api/v1/users - creates user with provided name and email

{

  "name": "string",
  
  "email": "string"
  
}

GET /api/v1/users/{email} - returns the info for user with provided email

PATCH /api/v1/users/{email} - update information for user with provided email

{

  "name": "string",
  
  "is_active": true,
  
  "is_superuser": false
  
}

## Getting started

The root directory should contain ".env.dev.ya" file with the content:

YANDEX_CLIENT_ID=<your_YANDEX_CLIENT_ID>

YANDEX_CLIENT_SECRET=<your_YANDEX_CLIENT_SECRET>

wich can be obtained on https://oauth.yandex.ru/client/new

The callback endpoint for dev - http://localhost:8000/auth/yandex/callback

To install all dependencies:

```sh
pip install -r requirements.txt
```

To start Docker from main directory:

```sh
$ docker compose -f docker_compose_dev.yaml --env-file .env.dev.pg up -d

```

To make migrations:

```sh
$ alembic upgrade head

```

To start app:

```sh
$ python3 main.py

```
