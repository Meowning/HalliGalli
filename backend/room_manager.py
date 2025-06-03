import random
from collections import deque, Counter

class RoomManager:
    def __init__(self):
        self.rooms = {}

    def create_room(self, data):
        room_id = data.get("roomId") or str(random.randint(1000, 9999))
        room_name = data.get("name", room_id)

        self.rooms[room_id] = {
            "hostId": data["userId"],
            "name": room_name,
            "players": {
                data["userId"]: {
                    "nickname": data["nickname"],
                    "deck": None,
                    "faceUpPile": []
                }
            },
            "turnOrder": [],
            "currentTurn": 0,
            "centralPile": [],
            "bellPile": [],
            "status": "waiting"
        }
        return room_id

    def join_room(self, data):
        room_id = data["roomId"]
        user_id = data["userId"]
        nickname = data["nickname"]

        if room_id not in self.rooms:
            return False, "방 없음"

        room = self.rooms[room_id]
        if room["status"] != "waiting":
            return False, "이미 시작됨"
        if user_id in room["players"]:
            return False, "이미 입장됨"

        room["players"][user_id] = {
            "nickname": nickname,
            "deck": None,
            "faceUpPile": []
        }
        return True, ""

    def leave_room(self, user_id):
        for room_id, room in list(self.rooms.items()):
            if user_id in room["players"]:
                del room["players"][user_id]
                room["turnOrder"] = [pid for pid in room["turnOrder"] if pid != user_id]

                if room["hostId"] == user_id:
                    if room["turnOrder"]:
                        room["hostId"] = room["turnOrder"][0]
                    else:
                        del self.rooms[room_id]
                        continue

                if room["status"] == "running" and len(room["turnOrder"]) <= 1:
                    room["status"] = "ended"

                if not room["players"]:
                    del self.rooms[room_id]
        return True, ""

    def serialize(self):
        return [
            {
                "roomId": rid,
                "name": room["name"],
                "playerCount": len(room["players"])
            }
            for rid, room in self.rooms.items()
        ]

    def get_players(self, room_id):
        room = self.rooms.get(room_id)
        if not room:
            return {}

        return {
            "hostId": room["hostId"],
            "players": [
                {
                    "id": pid,
                    "nickname": info["nickname"],
                    "remainingCards": len(info["deck"]) if info["deck"] is not None else 0,
                    "latestCard": info["faceUpPile"][-1] if info["faceUpPile"] else None
                }
                for pid, info in room["players"].items()
            ]
        }

    def can_start_game(self, room_id, user_id):
        room = self.rooms.get(room_id)
        if not room:
            return False, "방 없음"
        if room["hostId"] != user_id:
            return False, "호스트만 가능"
        if len(room["players"]) < 2 or len(room["players"]) > 6:
            return False, "플레이어 수 2~6"
        return True, ""

    def start_game(self, room_id):
        room = self.rooms[room_id]
        room["status"] = "running"

        fruits = ["🍓", "🍌", "🥝", "🍇"]
        deck = []
        for fruit in fruits:
            deck += [{"fruit": fruit, "count": 1}] * 5
            deck += [{"fruit": fruit, "count": 2}] * 3
            deck += [{"fruit": fruit, "count": 3}] * 3
            deck += [{"fruit": fruit, "count": 4}] * 2
            deck += [{"fruit": fruit, "count": 5}] * 1
        random.shuffle(deck)

        player_ids = list(room["players"].keys())
        num_players = len(player_ids)
        per = len(deck) // num_players
        leftover_start = per * num_players

        for i, pid in enumerate(player_ids):
            start_idx = i * per
            end_idx = start_idx + per
            room["players"][pid]["deck"] = deque(deck[start_idx:end_idx])
            room["players"][pid]["faceUpPile"] = []

        room["bellPile"] = deck[leftover_start:]
        room["turnOrder"] = player_ids[:]
        room["currentTurn"] = 0
        room["centralPile"] = []

    def play_card(self, room_id, player_id):
        room = self.rooms.get(room_id)
        if not room or room["status"] != "running":
            return False, "게임 중 아님"
        if room["turnOrder"][room["currentTurn"]] != player_id:
            return False, "차례 아님"
        player = room["players"][player_id]
        if not player["deck"]:
            return False, "카드 없음"

        card = player["deck"].popleft()
        player["faceUpPile"].append(card)
        room["centralPile"].append(card)
        room["currentTurn"] = (room["currentTurn"] + 1) % len(room["turnOrder"])
        return True, card

    def ring_bell(self, room_id, player_id):
        room = self.rooms.get(room_id)
        if not room or room["status"] != "running":
            return False, "게임 중 아님"

        counter = Counter()
        for c in room["centralPile"]:
            counter[c["fruit"]] += c["count"]

        winner = None
        for fruit, total in counter.items():
            if total >= 5:
                winner = player_id
                break

        if winner:
            won_count = len(room["centralPile"])
            for c in room["centralPile"]:
                room["players"][winner]["deck"].append(c)
            for pid in room["players"]:
                room["players"][pid]["faceUpPile"].clear()
            room["centralPile"].clear()
            return True, {"type": "success", "winner": winner, "wonCount": won_count}
        else:
            loser = player_id
            if not room["players"][loser]["faceUpPile"]:
                return False, "낼 카드 없음"
            penalty_card = room["players"][loser]["faceUpPile"].pop(0)
            room["bellPile"].append(penalty_card)
            return True, {"type": "fail", "loser": loser, "penaltyCard": penalty_card}

    def eliminate_check(self, room_id):
        room = self.rooms.get(room_id)
        eliminated = []
        for pid in list(room["turnOrder"]):
            if not room["players"][pid]["deck"]:
                eliminated.append(pid)
                room["turnOrder"].remove(pid)
        return eliminated

    def check_game_end(self, room_id):
        room = self.rooms.get(room_id)
        if room["status"] != "running":
            return None
        if len(room["turnOrder"]) == 1:
            winner = room["turnOrder"][0]
            room["status"] = "ended"
            return winner
        return None
