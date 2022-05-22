# Flask Group Chat

In messaging applications, sent messages pass through servers that we cannot control. If these servers are not open-sourced, one cannot be sure of their information's privacy. This application addresses aforementioned issue by providing open-source server application that people can host on their machine to communicate with their loved ones. They can choose between hosting to public internet or only to their local network.

Users should create an account to enter the application. Messaging happens in chat rooms. Each user can create unlimited number of rooms or they can join previously created ones. Messages are broadcasted to the room's participants. 

User accounts and chat rooms are protected by passwords. These passwords are hashed before storing in databases.

## Requirements

* Python 3
* Pip 3

## Running Server Locally

1. Install Python dependencies
    ```sh
    pip3 install -r requirements.txt
    ```
1. Initiate the Sqlite3 database with flask CLI command
    ```sh
    flask init-db
    ```
1. [OPTIONAL] Insert mock data to database for test purposes. All mock passwords are `1234`.
    ```sh
    flask import-mock-data
    ```
1. Start the Flask server
    ```sh
    python app.py
    ```
1. Access the application from browser
    ```sh
    http://localhost:5000
    ```

## Routes

| Route | Description | Methods |
|:---:|---|:---:|
| /auth/register | Interface where user creates an account. | GET, POST |
| /auth/login | Interface where user enters the application with his account. | GET, POST |
| /auth/logout | Logouts from the user's account and clears the session. | GET |
| /create-room | Interface where user creates unique chat rooms. | GET, POST |
| /join-room | Interface where user joins previously created chat rooms. | GET, POST |
| /live-chat | Interface of a chat room. People send messages to other people in the room. | GET, POST |
| /leave-chat | User leaves the chat room. User is redirected to index page. | GET |

## Application Interface

* Create account

    <img src="images/register.png"
             alt="An interface to register to the website."
             style="margin: 10px 30px; max-width: 600px; border: 1px solid grey;" />

* Login

    <img src="images/login.png"
         alt="An interface to login with registered account."
         style="margin: 10px 30px; max-width: 600px; border: 1px solid grey;" />

* Create chat room

    <img src="images/create_room.png"
         alt="An interface to create unique chat room."
         style="margin: 10px 30px; max-width: 600px; border: 1px solid grey;" />

* Join chat room

    <img src="images/join_room.png"
         alt="An interface to join previously created rooms."
         style="margin: 10px 30px; max-width: 600px; border: 1px solid grey;" />

* Live chat page

    <img src="images/live_chat.png"
         alt="An interface to message with others in the room."
         style="margin: 10px 30px; max-width: 600px; border: 1px solid grey;" />

## Technologies

* [Python Flask](https://flask.palletsprojects.com/en/2.1.x/quickstart/) back-end
* [Jinja2](https://jinja.palletsprojects.com/en/3.1.x/templates/) template engine for Flask
* HTML, CSS, JS front-end
* [Bootstrap 5.1](https://getbootstrap.com/docs/5.1/getting-started/introduction/) CSS framework
* [Socket.io](https://socket.io/docs/v4/client-api/) JS client API and [flask-socketio](https://flask-socketio.readthedocs.io/en/latest/getting_started.html) library
* [Sqlite3](https://www.sqlite.org/about.html) database
