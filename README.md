# Description

The `chat-room-api` is an API devloped with `Django` and `Django Rest Framework` in addition to other libraries and tools. The idea of this project is to serve as a back-end for a Chat Room (front-end web application) with similarities to ***[Discord](https://discord.com/)*** or similar platforms, in which registered users can join existing chat rooms or create their own and chat with peers. The `chat-room-API` allows for chat rooms, users and messages to be filtered or searched by query params. Token-based autheticated request ara available and are mandatory to ensure teh correct permissions and authorization for users based on their roles.
<br><br>


# Installation

### Clone The Repository

```bash
git clone https://github.com/Eadwulf/chat-room-api
```

### Change Directory

```bash
cd chat-room-api
```

### Install The Dependencies And Activate The Virtual Environment

```bash
pipenv install && pipenv shell
```

<aside>
    💡 Make sure to install <a href="https://pypi.org/project/pipenv/">pipenv</a> on your system
</aside>
<br><br>


# Database Setup

The project uses a PostgreSQL database. Configured as follows

```python
DATABASES = {
    'default': {
	'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DATABASE_NAME'),
        'HOST': env('DATABASE_HOST'),
        'PORT': env('DATABASE_PORT'),
        'USER': env('DATABASE_USER'),
        'PASSWORD': env('DATABASE_PASSWORD'),
    },
}
```

<aside>
    💡 If you do not have an existing database and user to use with these settings, follow the
    instructions bellow and create new ones.
</aside>
<br>

### Enter The PostgreSQL Prompt

```sql
psql -U postgres -d postgres
```

### Create The Database

```sql
CREATE DATABASE <database_name>;
```

### Create The User

```sql
CREATE USER <username> WITH ENCRYPTED PASSWORD '<password>';
```

### Modifying Connection Parameters

```sql
ALTER ROLE <database_user> SET client_encoding TO 'utf8';
ALTER ROLE <database_user> SET default_transaction_isolation TO 'read committed';
ALTER ROLE <database_user> SET timezone TO 'UTC';
```

### Grant Permissions To The User

```sql
 GRANT ALL PRIVILEGES ON DATABASE <database_name> TO <username>;
```

### Exit The Prompt

```sql
\q
```
<br>


# Environment Variables

### Create The Environment Variables File **(.env)**

In the root directory *(chat-room-api/)*, create the **.env** file and add to it the following

```python
DEBUG=<boolean_value>
SECRET_KEY=<your_django_api_key>
DATABASE_NAME=<your_database_name>
DATABASE_HOST=<your_database_host>
DATABASE_PORT=<your_database_port>
DATABASE_USER=<your_database_user>
DATABASE_PASSWORD=<your_database_password>
```
<aside>
    💡 Be aware that <em>django-environ</em> is required. Such dependency should be installed
    by running <em>pipenv install</em>
</aside>
<br>

### Apply the migrations

```python
python manage.py migrate
```
<br>

# Tests

I have created a total of 29 tests, that test the apps `api`, `chatrooms`, and `accounts`.
<br>

### Run the tests
```bash
python manage.py test
```

It should return an output such as

```bash
Found 29 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
.............................
----------------------------------------------------------------------
Ran 29 tests in 10.742s

OK
Destroying test database for alias 'default'...
```
<br>

### Tests in api app
A total of 26 tests were included. Each functionality of the endpoints in the API is tested.
The requests made in the tests to the API endpoints are token-based authenticated requests.
<br>

### Tests in the chatrooms app
The tests in the chatrooms app perform CRUD operations in the models Chatroom and Message.
<br>

### Tests in the accounts app
The test in the account app performs CRUD operations in the model CustomUser.
<br> <br>
# API Endpoints

The project consists of a total of eleven (11) endpoints, such endpoints provide functionalities for users, chatrooms, messages and more.

### Endpoints list

| URL | ALLOWED HTTP METHODS |
| --- | --- |
| api/users | GET, POST |
| api/users/{userId} | PATCH, PUT, DELETE |
| api/messages | GET, POST |
| api/messages/{messageId} | PATCH, PUT, DELETE |
| api/chatrooms | GET, POST |
| api/chatrooms/{chatroomId} | PATCH, PUT, DELETE |
| api/chatrooms/{chatroomId}/messages | GET, POST |
| api/chatrooms/{chatroomId}/Admins | GET, POST, DELETE |
| api/chatrooms/{chatroomId}/participants | GET, POST, DELETE |

### api/users

| HTTP METHOD | REQUIRED DATA | ACTION | STATUS CODE |
| --- | --- | --- | --- |
| GET |  | Retrieves the list of users | 200 |
| POST | username, password | Creates a user | 201 |

### api/users/{userId}

| HTTP METHOD | REQUIRED DATA | ACTION | STATUS CODE |
| --- | --- | --- | --- |
| GET |  | Retrieves the details of the user | 200 |
| PATCH | Any field | Partially updates the user data | 200 |
| PUT | All fields | Updates the user data | 200 |
| DELETE |  | Deletes the user | 204 |

### api/messages

| HTTP METHOD | REQUIRED DATA | ACTION | STATUS CODE |
| --- | --- | --- | --- |
| GET |  | Retrieves the list of messages | 200 |
| POST | chatroom_id, sender_id, body | Creates a message | 201 |

### api/messages/{messageId}

| HTTP METHOD | REQUIRED DATA | ACTION | STATUS CODE |
| --- | --- | --- | --- |
| GET |  | Retrieves the details of the message | 200 |
| PATCH | Any field | Partially updates the message data | 200 |
| PUT | All fields | Updates the message data | 200 |
| DELETE |  | Deletes the message | 204 |

### api/chatrooms

| HTTP METHOD | REQUIRED DATA | ACTION | STATUS CODE |
| --- | --- | --- | --- |
| GET |  | Retrieves the list of chatrooms | 200 |
| POST | name | Creates a chatroom | 201 |

### api/chatrooms/{chatroomId}

| HTTP METHOD | REQUIRED DATA | ACTION | STATUS CODE |
| --- | --- | --- | --- |
| GET |  | Retrieves the details of the chatroom | 200 |
| PATCH | Any field | Partially updates the chatroom data | 200 |
| PUT | All fields | Updates the chatroom data | 200 |
| DELETE |  | Deletes the chatroom | 204 |

### api/chatrooms/{chatroomId}/messages

| HTTP METHOD | REQUIRED DATA | ACTION | STATUS CODE |
| --- | --- | --- | --- |
| GET |  | Retrieves the list of messages associated with the chatroom | 200 |
| POST | body | Creates a message and adds it to the chatroom | 200 |

<aside>
    💡 The <em><strong>DELETE</strong></em> method can be call on the message object by using the <em><strong>api/messages/{messageId}</strong></em> endpoint.
</aside>

### api/chatrooms/{chatroomId}/admins

| HTTP METHOD | REQUIRED DATA | ACTION | STATUS CODE |
| --- | --- | --- | --- |
| GET |  | Retrieves the list of admins associated with the chatroom | 200 |
| POST | id | Adds the admins to the chatroom | 200 |
| DELETE | id | Removes the admins from the chatroom | 200 |

### api/chatrooms/{chatroomId}/participants

| HTTP METHOD | REQUIRED DATA | ACTION | STATUS CODE |
| --- | --- | --- | --- |
| GET |  | Retrieves the list of participants associated with the chatroom | 200 |
| POST | id | Adds the participant to the chatroom | 200 |
| DELETE | id | Removes the participant from the chatroom | 200 |
