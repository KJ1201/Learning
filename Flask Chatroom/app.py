from website import create_app, socketio

app = create_app()

if __name__ == "__main__":
    socketio.run(app, debug=True)


'''
To Do:
- Create a database to store messages
- Create proper authentication systems
- Create a public portal for it

Reference:
TechwithTim
'''