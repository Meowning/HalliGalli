import os
import uuid
from flask import Flask, send_from_directory, request, redirect, session
from flask_cors import CORS
from flask_session import Session
from flask_socketio import SocketIO, emit, join_room, leave_room
from models import db, ChatLog, VisitLog, User
from room_manager import RoomManager

app = Flask(__name__, static_folder="static", static_url_path="/")
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret-key")
DB_HOST = os.getenv("DB_HOST", "mysql")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "halligalli")
DB_USER = os.getenv("DB_USER", "halligalli")
DB_PASSWORD = os.getenv("DB_PASSWORD", "halligalli")

app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SESSION_TYPE"] = "sqlalchemy"
app.config["SESSION_SQLALCHEMY"] = db
app.config["SESSION_SQLALCHEMY_TABLE"] = "flask_sessions"
app.config["SESSION_PERMANENT"] = False

db.init_app(app)
Session(app)
CORS(app, supports_credentials=True)

socketio = SocketIO(app, cors_allowed_origins="*", logger=True, engineio_logger=True)

rooms = RoomManager()


def get_or_set_user_id():
    user_id = session.get("user_id")
    if not user_id:
        user_id = str(uuid.uuid4())
        session["user_id"] = user_id
        new_user = User(user_id=user_id, nickname=session.get("nickname", ""))
        db.session.add(new_user)
        db.session.commit()
    return user_id


@app.route("/api/enter_nickname", methods=["GET", "POST"])
def enter_nickname():
    if request.method == "POST":
        nickname = request.form.get("nickname", "").strip()
        if not nickname:
            return "닉네임을 입력해주세요", 400

        session["nickname"] = nickname
        user_id = get_or_set_user_id()
        user = User.query.get(user_id)
        if user:
            user.nickname = nickname
        else:
            new_user = User(user_id=user_id, nickname=nickname)
            db.session.add(new_user)
        db.session.commit()
        return "", 200

    return """
    <form method="POST" action="/api/enter_nickname">
      <input type="text" name="nickname" placeholder="닉네임 입력" />
      <button type="submit">입장</button>
    </form>
    """


@app.route("/api/lobby")
def lobby():
    if "user_id" not in session or "nickname" not in session:
        return redirect("/api/enter_nickname")
    return send_from_directory(app.static_folder, "index.html")


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_frontend(path):
    if "user_id" not in session or "nickname" not in session:
        return redirect("/api/enter_nickname")
    if path and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, "index.html")


@socketio.on("connect")
def on_connect():
    user_id = get_or_set_user_id()
    visit = VisitLog(user_id=user_id, path="/socket_connect")
    db.session.add(visit)
    db.session.commit()
    emit("me", {"userId": user_id}, room=request.sid)


@socketio.on("room/create")
def on_create(data):
    user_id = get_or_set_user_id()
    nickname = session.get("nickname", "익명")
    data["userId"] = user_id
    data["nickname"] = nickname

    room_id = rooms.create_room(data)
    join_room(room_id)

    visit = VisitLog(user_id=user_id, path=f"/room/{room_id}/create")
    db.session.add(visit)
    db.session.commit()

    emit("room/create/success", {"roomId": room_id}, room=request.sid)
    emit("room/list", rooms.serialize(), broadcast=True)
    emit("room/players", rooms.get_players(room_id), room=room_id)


@socketio.on("room/join")
def on_join(data):
    user_id = get_or_set_user_id()
    nickname = session.get("nickname", "익명")
    data["userId"] = user_id
    data["nickname"] = nickname
    room_id = data.get("roomId")

    success, msg = rooms.join_room(data)
    if not success:
        emit("room/error", {"msg": msg}, room=request.sid)
        if msg == "이미 입장됨":
            join_room(room_id)
            emit("room/players", rooms.get_players(room_id), room=room_id)
            emit("room/list", rooms.serialize(), broadcast=True)
        return

    emit("room/join/success", {"roomId": room_id}, room=request.sid)
    join_room(room_id)

    visit = VisitLog(user_id=user_id, path=f"/room/{room_id}/join")
    db.session.add(visit)
    db.session.commit()

    emit("room/players", rooms.get_players(room_id), room=room_id)
    emit("room/list", rooms.serialize(), broadcast=True)


@socketio.on("room/list")
def on_room_list():
    emit("room/list", rooms.serialize())


@socketio.on("game/start")
def on_game_start(data):
    user_id = get_or_set_user_id()
    data["userId"] = user_id
    room_id = data.get("roomId")

    ok, msg = rooms.can_start_game(room_id, user_id)
    if not ok:
        emit("game/error", {"msg": msg}, room=request.sid)
        return

    rooms.start_game(room_id)
    visit = VisitLog(user_id=user_id, path=f"/room/{room_id}/start")
    db.session.add(visit)
    db.session.commit()

    first_pid = rooms.rooms[room_id]["turnOrder"][0]
    success, card = rooms.play_card(room_id, first_pid)
    if not success:
        card = None

    emit("game/start", {}, room=room_id)
    emit("room/players", rooms.get_players(room_id), room=room_id)
    if card is not None:
        emit("card-played", {"playerId": first_pid, "card": card}, room=room_id)


@socketio.on("play-card")
def on_play_card(data):
    user_id = get_or_set_user_id()
    room_id = data.get("roomId")

    success, result = rooms.play_card(room_id, user_id)
    if not success:
        emit("play-error", {"msg": result}, room=room_id)
        return

    card = result
    emit("card-played", {"playerId": user_id, "card": card}, room=room_id)

    eliminated = rooms.eliminate_check(room_id)
    if eliminated:
        for pid in eliminated:
            emit("player-eliminated", {"playerId": pid}, room=room_id)

    winner = rooms.check_game_end(room_id)
    if winner:
        emit("game-end", {"winnerId": winner}, room=room_id)


@socketio.on("ring-bell")
def on_ring_bell(data):
    user_id = get_or_set_user_id()
    room_id = data.get("roomId")

    success, result = rooms.ring_bell(room_id, user_id)
    if not success:
        emit("bell-error", {"msg": result}, room=room_id)
        return

    if result["type"] == "success":
        emit(
            "bell-success",
            {"winnerId": result["winner"], "wonCount": result["wonCount"]},
            room=room_id,
        )
    else:
        emit(
            "bell-fail",
            {"loserId": result["loser"], "penaltyCard": result["penaltyCard"]},
            room=room_id,
        )

    eliminated = rooms.eliminate_check(room_id)
    if eliminated:
        for pid in eliminated:
            emit("player-eliminated", {"playerId": pid}, room=room_id)

    winner = rooms.check_game_end(room_id)
    if winner:
        emit("game-end", {"winnerId": winner}, room=room_id)


@socketio.on("chat/message")
def on_chat(data):
    user_id = get_or_set_user_id()
    nickname = session.get("nickname", "익명")

    chat_log = ChatLog(
        room_id=data["roomId"],
        user_id=user_id,
        nickname=nickname,
        text=data.get("text", "")
    )
    db.session.add(chat_log)
    db.session.commit()

    data["userId"] = user_id
    data["nickname"] = nickname
    emit("chat/message", data, room=data["roomId"])


@socketio.on("room/leave")
def on_leave(data):
    user_id = get_or_set_user_id()
    room_id = data.get("roomId")

    if room_id in rooms.rooms and user_id in rooms.rooms[room_id]["players"]:
        leave_room(room_id)

    success, msg = rooms.leave_room(user_id)
    if not success:
        emit("room-error", {"msg": msg}, room=request.sid)
        return

    emit("room/list", rooms.serialize(), broadcast=True)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    socketio.run(app, host="0.0.0.0", port=5000, debug=True)
