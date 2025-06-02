from flask import Flask, send_from_directory
from flask_socketio import SocketIO, emit, join_room
from game.room_manager import RoomManager

app = Flask(__name__, static_folder="../frontend", static_url_path="/")
socketio = SocketIO(app, cors_allowed_origins="*")
rooms = RoomManager()

@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

# 소켓 통신
@socketio.on("room/create")
def on_create(data):
    room_id = rooms.create_room(data)
    join_room(room_id)
    emit("room/list", rooms.serialize(), broadcast=True)
    emit("room/players", rooms.get_players(room_id), room=room_id)

@socketio.on("room/join")
def on_join(data):
    success, msg = rooms.join_room(data)
    if not success:
        emit("room/error", {"msg": msg})
        return
    join_room(data["roomId"])
    emit("room/players", rooms.get_players(data["roomId"]), room=data["roomId"])

@socketio.on("room/list")
def on_room_list():
    emit("room/list", rooms.serialize())

@socketio.on("game/start")
def on_game_start(data):
    room_id = data["roomId"]
    user_id = data["userId"]
    ok, msg = rooms.can_start_game(room_id, user_id)
    if not ok:
        emit("game/error", {"msg": msg})
        return
    emit("game/start", {"roomId": room_id}, room=room_id)

@socketio.on("chat/message")
def on_chat(data):
    emit("chat/message", data, room=data["roomId"])

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=5000)

