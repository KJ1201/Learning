from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from flask_socketio import join_room, leave_room, send
from . import rooms, generate_unique_code

views = Blueprint("views", __name__)

@views.route("/", methods=["GET", "POST"])
def home():
    session.clear()
    if request.method=="POST":
        name = request.form.get("name")
        code = request.form.get("code")
        join = request.form.get("join", False)
        create = request.form.get("create", False)
        
        if len(name) < 2:
            flash('Please enter a name.', "error")
            return render_template("home.html", code=code, name=name)

        if join != False and not code:
            flash('Please enter a room code.', "error")
            return render_template("home.html", code=code, name=name)
            
        room = code
        if create != False:
            room = generate_unique_code(4)
            rooms[room] = {"members" : 0, "messages": []}
           
        elif code not in rooms:
            flash("Room does not exists.", "error")
            return render_template("home.html", code=code, name=name)
            
        session["room"] = room
        session["name"] = name
        return redirect(url_for("views.room"))
        

    return render_template("home.html")


@views.route('/room')
def room():
    room = session.get("room")
    if room is None or session.get("name") is None or room not in rooms:
        return redirect(url_for("views.home"))
    
    return render_template("room.html", room=room, messages=rooms[room]["messages"])