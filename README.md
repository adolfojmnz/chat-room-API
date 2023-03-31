# Description

The `chat-room-api` is an API developed with `Django` and `Django Rest Framework` in addition to other libraries and tools. The idea of this project is to serve as a back-end for a Chat Room (front-end web application) with similarities to ***[Discord](https://discord.com/)*** or similar platforms, in which registered users can join existing chat rooms or create their own and chat with peers. The `chat-room-API` allows for chat rooms, users and messages to be filtered or searched by query params. The API supports token-based authenticated requests and, it's a must to ensure that all the permission and authorization functionalities are applied to the users based on their roles.
<br><br>


# Installation

<aside>💡 Both Docker and DockerCompose are required </aside>
<br>

### Clone The Repository
```console
git clone https://github.com/Eadwulf/chat-room-api
```

### Change Directory
```console
cd chat-room-api
```

### Checkout `docker` branch
```console
git checkout docker
```

### Build/Run the containers
```console
docker-compose up -d
```

### Run the tests
```console
docker exec -it chat-room-api python manage.py test
```

### PostgreSQL Prompt
<aside>💡 If you need to access the PostgreSQL prompt </aside>

```console
docker exec -it chat-room-db psql -U postgres -d postgres
```
<br>


# API Endpoints

The project consists of a total of ten (10) endpoints, such endpoints provide functionalities for users, chatrooms, messages and more.

### Endpoints list

| URL | ALLOWED HTTP METHODS |
| --- | --- |
| api/users | GET, POST |
| api/users/{userId} | GET, PATCH, PUT, DELETE |
| api/users/{userId}/friends | GET, POST, DELETE |
| api/messages | GET, POST |
| api/messages/{messageId} | GET, PATCH, PUT, DELETE |
| api/chatrooms | GET, POST |
| api/chatrooms/{chatroomId} | GET, PATCH, PUT, DELETE |
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

### api/users/{userId}/friends

| HTTP METHOD | REQUIRED DATA | ACTION | STATUS CODE |
| --- | --- | --- | --- |
| GET |  | Retrieves the user's friend list | 200 |
| POST | | Adds a friend to the user's friend list | 200 |
| DELETE | | Deletes a friend from the user's friend list | 200 |

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
    💡 The <em><strong>DELETE</strong></em> method can be called on the message object by using the <em><strong>api/messages/{messageId}</strong></em> endpoint.
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
