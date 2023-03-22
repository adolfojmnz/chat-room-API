# Description

The `chat-room-api` is a personal project developed to showcase my abilities in the back-end development field. For this project, I have developed an API with `Django` and `Django Rest Framework` in addition to other libraries and tools. The idea of this project is to serve as a back-end for a Chat Room (front-end web application) with similarities to ***[Discord](https://discord.com/)*** or similar platforms, in which registered users can join existing chat rooms or create their own and chat with peers. The `chat-room-API` allows for a chat room to have multiple topics selected, so it can be searched or filtered not only through its name but also through its topics’ names.
<br><br>


# Project Structure

The project consists of two apps, `accounts`, and `chatrooms` as well as the project package, `config`.

### **The accounts app**

This app holds the model `CustomUser`, a class that inherits `django.contrib.auth.models.AbstractUser`.  The model `CustomUser` possesses the following attributes

The default ones that the `django.contrib.auth.models.AbstractUser` inheritance provide

```python
username
first_nam
last_nam
email
password
group
user_permissions
is_staff
is_active
is_superuser
last_login
date_joined
```

And two extra fields that I included

```python
bio
birthdate
```

### The chatrooms app

This apps holds three models, `Chatroom`, `Message`, and `Topic`, which are the backbone of the API
<br><br>


# Installation

**Clone the repository**

```jsx
git clone https://github.com/Eadwulf/chat-room-api
```

**Change directory**

```jsx
cd chat-room-api
```

**Install the dependencies and activate the virtual environment**

```jsx
pipenv install && pipenv shell
```

<aside>💡 Make sure to install [pipenv](https://pypi.org/project/pipenv/) on your system</aside>
<br><br>

# Database Setup

**The default database settings are**

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

**Alternatively, you can set up a more robust database such as PostgreSQL**

```python
DATABASES = {
    'default': {
				'ENGINE': 'django.db.backends.postgresql',
        'NAME': '<database_name>',
        'HOST': 'localhost',
        'PORT': '5432',
        'USER': '<username>',
        'PASSWORD': '<password>',
    },
}
```

**Apply the migrations**

```python
python manage.py migrate
```
<br>

# Environment Variables

**The .env file**

Create a .env file in the root directory *(chat-room-api/.env)* and add to it the following

```python
DEBUG=True
SECRET_KEY=<your_django_api_key>
```

<aside>💡 Be aware that `django-environ`. Such dependency should be installed by running `pipenv install`</aside>
<br><br>

# API Endpoints

Each endpoint requires a SimpleJWT Token for authorization. Pass the token in the header of the request such as

```python
{'Authorization': 'JWT <token>'}
```