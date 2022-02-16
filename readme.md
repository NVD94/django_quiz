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

The REST APIs to the quiz app is described below.

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

`POST /quizzes`

    curl --location --request POST 'http://127.0.0.1:8000/quizzes' \
    --header 'Authorization: Token your_token' \
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
    --header 'Authorization: Token your_token'

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

## Get scores of the created quizzes

### Request

`GET /quizzes{quizz_id}/scores`.

    curl --location --request GET 'http://127.0.0.1:8000/quizzes/36/scores' \
    --header 'Authorization: Token your_token'


### Body Response

    [
        {
            "score": 75.0,
            "user": {
                "email": "test@testtest"
            }
        },
        {
            "score": 50.0,
            "user": {
                "email": "test2@testtest"
            }
        }
    ]

## Get my participations

### Request

`GET /participations?`.
`GET /participations?filter={filter_value_for_quiz_name}`.

    curl --location --request GET 'http://127.0.0.1:8000/participations' \
    --header 'Authorization: Token your_token'


### Body Response

    [
        {
            "id": 3,
            "quiz": {
                "name": "First quiz",
                "created": "2022-02-15T19:22:37.178565Z"
            },
            "progress": "COMPLETED"
        },
        {
            "id": 4,
            "quiz": {
                "name": "Second quiz",
                "created": "2022-02-15T18:10:15.110548Z"
            },
            "progress": "COMPLETED"
        },

        {
            "id": 15,
            "quiz": {
                "name": "Third quiz",
                "created": "2022-02-15T19:22:37.178565Z"
            },
            "progress": "IN_PROGRESS1/2"
        }
    ]

## Get score of a participation

### Request

`GET /participations/{participation_id}/progress`.

    curl --location --request GET 'http://127.0.0.1:8000/participations/3/progress' \
    --header 'Authorization: Token your_token'


### Body Response

    {
        "progress": "NOT_STARTED"
    }

## Get quiz by participation id

### Request

`GET /participations/{participation_id}/quiz`.

    curl --location --request GET 'http://127.0.0.1:8000/participations/3/quiz' \
    --header 'Authorization: Token your_token'


### Body Response

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

## Filter created, quizzes, invited users, questions (to complete)

### Request

`GET /search`.
`GET /search?filter={filter_value}`.

    curl --location --request GET 'http://127.0.0.1:8000/participations/3/progress' \
    --header 'Authorization: Token your_token'


### Body Response

    {
    "quizzes": [
            {
                "id": 35,
                "name": "Second quiz",
                "summary": "This is just for testing"
            }
        ]
    }

## Select answer

### Request

`POST /participations/{participation_id}}/answers/{answer_id}`.

    curl --location --request POST 'http://127.0.0.1:8000/participations/15/answers/18' \
    --header 'Authorization: Token your_token'


### Body Response

    {
        "message": "Answer successfuly selected"
    }

## Invite user to the quiz

### Request

`POST /invite/{quiz_id}`.

    curl --location --request POST 'http://127.0.0.1:8000/invite/36' \
    --header 'Authorization: Token your_token' \
    --header 'Content-Type: application/json' \
    --data-raw '{"email": "test@test.test"}'


### Body Response

    {
        "message": "Invitation was successfully sent"
    }
