# ChatroomApplication
A website to host and manage multiple chat rooms made using HTML5, CSS3, JavaScript, JSON, AJAJ, Python, Flask and, SQLAlchemy.  

## Overview
This website allows the users to create, post messages to and, delete chatrooms. the users are required to create an account first and then login with their credentials to proceed. Each user can create multiple chatrooms and delete them as they please. A user can be in only one chatroom at a time. Multiple users can login to the chat site at the same time and exchange messages.


## How to run

Install Python 3.5, Flask, SQLAlchemy and, the Flask-SQLAlchemy extension.  
Open Command prompt on Windows or terminal on Mac.  
Set the FLASK_APP environment variable to your chat.py as: "set FLASK_APP=path/chat.py"  
Initialize the chat.db database using: "flask initdb"  
Run the application using: "flask run"  

## Specifications

When visiting the page for the first time, users will be given the chance to create an account or login.  
Once successfully logged in, the user will be given a list of possible chat rooms to join, or a message stating that none currently exist. The user will have the option to create a new chat room.  
Once in a chat room, the user will be shown the history of messages for that chat room, as well as be kept up to date as messages are sent to the chat room. The user will also have the option to post a new message to the chat room. The user can leave the chat room by clicking the leave chatroom button.  
Users can be in only one chat room at a time.  
The application uses AJAJ and JSON to update the list of messages posted to the chat room, and to post new messages to the chat room.  
All AJAJ chat updates will only send new messages to the user.   
The application does polling to ensure that new messages are always available to the user. The application polls every alternate second.  
Once a user leaves the chat room, they will again be shown a list of potential chat rooms to join (or a message if none exist).  
The user will also have the option to delete any chat rooms that they created by clicking on the delete button for that chatroom.  
Any users still in a room when it is deleted will be shown a message informing them that the room was deleted and will be redirected to their profiles.  
All data for this application will be stored in an SQLite database named "chat.db" using SQLAlchemy's ORM and the Flask-SQLAlchemy extension.  
