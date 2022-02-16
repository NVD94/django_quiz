# Quiz SaaS

This is a simple group of quiz apis that allow users to create quizzes, invite participants, and participate in a quiz

## Create a virtual environment inside the root folder, to isolate our package dependencies locally

    python3 -m venv env

    source env/bin/activate  # On Windows use `env\Scripts\activate`

## Install requirements

    pip install -r requirements.txt

## Setup you email account in settings.py to send the scores and invitations

    EMAIL_HOST = ""  # YOUR EMAIL HOST
    EMAIL_HOST_USER = ""  # YOUR EMAIL
    EMAIL_PORT = "" #Port specified by the email provider
    EMAIL_USE_TLS = False #This value migth change deppending on the email provider
    EMAIL_USE_SSL = True #This value migth change deppending on the email provider
    EMAIL_HOST_PASSWORD = ""  # YOUR EMAIL PASSWORD

## Create a super user

    python manage.py createsuperuser

## Run makemigrations and migrate to initiate the db

    python manage.py makemigrations
    python manage.py migrate

## Start the app

    python manage.py runserver

# REST API

The REST API to the quiz app is described below.

## Create user

### Request

`/auth/users/`

    curl --location --request POST 'http://127.0.0.1:8000/auth/users/' \
    --header 'Content-Type: application/json' \
    --data-raw '{"username":"test",
    "password":"test",
    "password2":"test",
    "email": "test@test.tes"
    }'

## Login

### Request

`/auth/users/`

    curl --location --request POST 'http://127.0.0.1:8000/auth/token/login/' \
    --header 'Content-Type: application/json' \
    --data-raw '{"username": "test",
    "password": "test"
    }'

## Create quiz

### Request

`/quizzes`

    curl --location --request POST 'http://127.0.0.1:8000/quizzes' \
    --header 'Authorization: Token 28abd7081cc631a18dbd8ddcc6b2995a401dfba2' \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "name":"Example quiz",
        "summary":"This is just an example",
        "questions": [
            {
                "content": "What is the capital of Portugal?",
                "answers": [
                    {
                    "content": "Porto",
                    "is_correct": false
                    },
                    {
                    "content": "Lisbon",
                    "is_correct": true
                    }
                ]
            },
            {
                "content": "What is the color of the sky?",
                "answers": [
                    {
                    "content": "Red",
                    "is_correct": false
                    },
                    {
                    "content": "Blue",
                    "is_correct": true
                    }
                ]
            }
        ]

    }'

## Get created quizzes

### Request

`GET /quizzes`

    curl --location --request GET 'http://127.0.0.1:8000/quizzes' \
    --header 'Authorization: Token youtoken'

### Response body

    [
        {
            "id": 36,
            "name": "Third quiz",
            "summary": "This is just for testing",
            "questions": [
                {
                    "id": 8,
                    "content": "What is the capital of Portugal?",
                    "answers": [
                        {
                            "id": 15,
                            "content": "Porto"
                        },
                        {
                            "id": 16,
                            "content": "Lisbon"
                        }
                    ]
                },
                {
                    "id": 9,
                    "content": "What is the color of the sky?",
                    "answers": [
                        {
                            "id": 17,
                            "content": "Red"
                        },
                        {
                            "id": 18,
                            "content": "Blue"
                        }
                    ]
                }
            ]
        }
    ]
