from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import login_manager
from flask_socketio import join_room, leave_room, send, SocketIO
import random
from string import ascii_uppercase

socketio = SocketIO()
db = SQLAlchemy()
DB_NAME = "database.db"

rooms = {}

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "helloworld"
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"

    db.init_app(app)
    socketio.init_app(app)

    from .views import views

    app.register_blueprint(views, url_prefix="/")

    return app

def generate_unique_code(length):
    while True:
        code = ""
        for _ in range(length):
            code += random.choice(ascii_uppercase)

        if code not in rooms:
            break

    return code

@socketio.on("connect")
def connect(auth):
    room = session.get("room")
    name = session.get("name")
    if not rooms or not name:
        return
    if not room in rooms:
        leave_room(room)
        return 
    
    join_room(room)
    send({"name" : name, "message" : "has entered the room"}, to=room)
    rooms[room]["members"] += 1
    print(f"{name} joined room {room}")
    
@socketio.on("message")
def message(data):
    room = session.get("room")
    if room not in rooms:
        return
    
    content = {
        "name": session.get("name"),
        "message": data["data"]
    }

    send(content, to=room)
    rooms[room]["messages"].append(content)
    print(f"{session.get("name")} said: {data['data']}")


@socketio.on("disconnect")
def disconnect():
    room = session.get("room")
    name = session.get("name")
    leave_room(room)

    if room in rooms:
        rooms[room]["members"] -= 1
        if rooms[room]["members"] <= 0:
            del rooms[room]

    send({"name" : name, "message" : "has left the room"}, to=room)
    print(f"{name} left room {room}")
