<template>
  <div class="game-room" :roomid="roomId">
    <div v-if="gameStarted" class="game-started-banner">
      🎉 게임이 시작되었습니다!
    </div>

    <ScoreBoard
      :players="players"
      :currentUserId="currentUserId"
      :currentTurnId="currentTurnId"
    />

    <div class="main-area">
      <div
        v-for="(player, idx) in players"
        :key="player.id"
        class="center-card-area"
        :class="{ 'my-turn': player.id === currentTurnId }"
        :style="getPlayerCardStyle(idx, players.length)"
        @click="tryPlayCard(player.id)"
      >
        <PlayerCard
          v-if="player.latestCard"
          :card="player.latestCard"
          :isCurrentTurn="player.id === currentUserId"
        />
        <div v-else class="card-back"></div>

        <div class="player-nickname">
          {{ player.nickname }} ({{ player.remainingCards }}장)
          <span v-if="player.id === currentTurnId" class="turn-label">← 내 턴</span>
        </div>
      </div>

      <button
        v-if="hostId && isHost && !gameStarted"
        class="start-button"
        :disabled="players.length < 2"
        @click="startGame"
      >
        {{ players.length < 2 ? "플레이어 2명 필요" : "게임 시작" }}
      </button>

      <div class="bell-wrapper">
        <BellButton @ring="ringBell" :disabled="!gameStarted" />
      </div>
    </div>

    <ChatBox
      :messages="visibleMessages"
      v-model:modelValue="chatInput"
      @send="sendMessage"
      @focusInput="onChatFocus"
      @blurInput="onChatBlur"
      class="chat-box-position"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from "vue";
import { io } from "socket.io-client";
import { useRoute, useRouter } from "vue-router";

import PlayerCard from "./PlayerCard.vue";
import BellButton from "./BellButton.vue";
import ChatBox from "./ChatBox.vue";
import ScoreBoard from "./ScoreBoard.vue";

const route = useRoute();
const router = useRouter();

const roomId = route.params.roomId;
const currentUserId = ref(null);
const hostId = ref(null);
const players = ref([]);
const currentTurnId = ref(null);
const gameStarted = ref(false);
const fullMessages = ref([]);
const visibleMessages = ref([]);
const chatInput = ref("");
let hideTimer = null;

let socket = null;

const isHost = computed(() => {
  return currentUserId.value === hostId.value;
});

const BACKEND_HOST = import.meta.env.VITE_BACKEND_HOST || window.location.hostname;
const BACKEND_PORT = import.meta.env.VITE_BACKEND_PORT || "5000";
const BACKEND_URL = `http://${BACKEND_HOST}:${BACKEND_PORT}`;

function getPlayerCardStyle(index, total) {
  const angle = (360 / total) * index - 90;
  const r = 200;
  const rad = (angle * Math.PI) / 180;
  return {
    position: "absolute",
    top: `calc(50% + ${r * Math.sin(rad)}px)`,
    left: `calc(50% + ${r * Math.cos(rad)}px)`,
    transform: "translate(-50%, -50%)",
  };
}

function tryPlayCard(playerId) {
  if (!gameStarted.value) {
    console.log("[GameRoom] 아직 게임 시작 전입니다.");
    return;
  }
  if (playerId !== currentUserId.value) {
    console.log("[GameRoom] 내 턴이 아닙니다.");
    return;
  }
  if (playerId !== currentTurnId.value) {
    console.log("[GameRoom] 서버가 알려준 순서와 다릅니다.");
    return;
  }
  console.log("[GameRoom] emit play-card:", playerId);
  socket.emit("play-card", {
    roomId
  });
}

function ringBell() {
  if (!gameStarted.value) {
    console.log("[GameRoom] 아직 게임 시작 전입니다.");
    return;
  }
  console.log("[GameRoom] emit ring-bell:", currentUserId.value);
  socket.emit("ring-bell", {
    roomId
  });
}

function receiveNewMessage(msg) {
  fullMessages.value.push(msg);
  visibleMessages.value = [msg];
  if (hideTimer) clearTimeout(hideTimer);
  hideTimer = setTimeout(() => {
    visibleMessages.value = [];
  }, 3000);
}

function sendMessage() {
  if (!chatInput.value.trim()) return;
  const newMsg = {
    id: Date.now(),
    nickname:
      players.value.find((p) => p.id === currentUserId.value)?.nickname ||
      "익명",
    text: chatInput.value,
    roomId,
  };
  console.log("[GameRoom] emit chat/message:", newMsg);
  socket.emit("chat/message", newMsg);
  receiveNewMessage(newMsg);
  chatInput.value = "";
}

function startGame() {
  console.log("[GameRoom] emit game/start by host", currentUserId.value);
  socket.emit("game/start", {
    roomId
  });
}

function onChatFocus() {
  visibleMessages.value = [...fullMessages.value];
  if (hideTimer) clearTimeout(hideTimer);
}
function onChatBlur() {
  if (hideTimer) clearTimeout(hideTimer);
  hideTimer = setTimeout(() => {
    visibleMessages.value = [];
  }, 3000);
}

onMounted(() => {
  socket = io(BACKEND_URL, {
    path: "/socket.io",
    transports: ["websocket"],
    withCredentials: true,
  });

  socket.on("me", (data) => {
    console.log("[GameRoom] received me:", data);
    currentUserId.value = data.userId;

    socket.emit("room/join", {
      roomId
    });
  });

  socket.on("connect", () => {
    console.log("[GameRoom] Socket connected to", BACKEND_URL);
  });

  socket.on("disconnect", () => {
    console.log("[GameRoom] Socket disconnected");
  });

  socket.on("room/players", (payload) => {
    console.log("[GameRoom] received room/players:", payload);
    // payload = { hostId, players: [ { id, nickname, remainingCards, latestCard }, … ] }
    if (payload.hostId !== undefined && Array.isArray(payload.players)) {
      hostId.value = payload.hostId;
      players.value = payload.players.map((p) => ({
        id: p.id,
        nickname: p.nickname,
        remainingCards: p.remainingCards,
        latestCard: null, // 이후 card-played 이벤트가 오면 업데이트
      }));
    } else {
      console.error("[GameRoom] 잘못된 room/players 페이로드:", payload);
    }
  });

  socket.on("room/join/success", (data) => {
    console.log("[GameRoom] received room/join/success:", data);
  });

  socket.on("game/start", () => {
    console.log("[GameRoom] received game/start");
    gameStarted.value = true;
  });

  socket.on("card-played", ({ playerId, card }) => {
    console.log("[GameRoom] received card-played:", playerId, card);
    const p = players.value.find((x) => x.id === playerId);
    if (p) {
      p.latestCard = card;
      p.remainingCards--;
    }
    const idx = players.value.findIndex((x) => x.id === playerId);
    if (idx >= 0 && players.value.length > 0) {
      const total = players.value.length;
      const nextIdx = (idx + 1) % total;
      currentTurnId.value = players.value[nextIdx].id;
    }
  });

  socket.on("bell-success", ({ winnerId, wonCount }) => {
    console.log("[GameRoom] received bell-success:", winnerId, wonCount);
    players.value.forEach((p) => {
      p.latestCard = null;
    });
    const w = players.value.find((x) => x.id === winnerId);
    if (w) {
      w.remainingCards += wonCount;
    }
    const idxW = players.value.findIndex((x) => x.id === winnerId);
    if (idxW >= 0 && players.value.length > 0) {
      const total = players.value.length;
      currentTurnId.value = players.value[(idxW + 1) % total].id;
    }
  });

  socket.on("bell-fail", ({ loserId }) => {
    console.log("[GameRoom] received bell-fail:", loserId);
    const p = players.value.find((x) => x.id === loserId);
    if (p) {
      p.remainingCards--;
    }
    const idxL = players.value.findIndex((x) => x.id === loserId);
    if (idxL >= 0 && players.value.length > 0) {
      const total = players.value.length;
      currentTurnId.value = players.value[(idxL + 1) % total].id;
    }
  });

  socket.on("player-eliminated", ({ playerId }) => {
    console.log("[GameRoom] received player-eliminated:", playerId);
    players.value = players.value.filter((x) => x.id !== playerId);
    if (currentTurnId.value === playerId && players.value.length > 0) {
      currentTurnId.value = players.value[0].id;
    }
  });

  socket.on("game-end", ({ winnerId }) => {
    console.log("[GameRoom] received game-end:", winnerId);
    const w = players.value.find((x) => x.id === winnerId);
    alert(`${w ? w.nickname : "알 수 없음"} 선수 승리!`);
  });

  socket.on("chat/message", (msg) => {
    console.log("[GameRoom] received chat/message:", msg);
    receiveNewMessage(msg);
  });

  socket.on("room/error", (e) => {
    console.warn("[GameRoom] room/error:", e);
    alert(e.msg || "방 관련 오류가 발생했습니다.");
  });
  socket.on("play-error", (e) => {
    console.warn("[GameRoom] play-error:", e);
    alert(e.msg || "카드 플레이 중 오류가 발생했습니다.");
  });
  socket.on("bell-error", (e) => {
    console.warn("[GameRoom] bell-error:", e);
    alert(e.msg || "종 치기 중 오류가 발생했습니다.");
  });
  socket.on("game/error", (e) => {
    console.warn("[GameRoom] game-error:", e);
    alert(e.msg || "게임 시작 중 오류가 발생했습니다.");
  });
});

onBeforeUnmount(() => {
  if (hideTimer) clearTimeout(hideTimer);
  if (socket) {
    socket.emit("room/leave", { roomId });
    socket.disconnect();
  }
});
</script>

<style scoped>
.game-room {
  position: relative;
  height: 100vh;
  background: #e6f0fa;
  padding: 1rem;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.game-started-banner {
  width: 100%;
  background-color: #ffeb3b;
  color: #333;
  padding: 0.5rem;
  text-align: center;
  font-weight: bold;
  margin-bottom: 1rem;
}

.main-area {
  position: relative;
  width: 80vw;
  max-width: 700px;
  height: 80vw;
  max-height: 700px;
  margin: 20px 0 10px;
  border-radius: 50%;
  overflow: hidden;
}

.center-card-area {
  width: 70px;
  height: 140px;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  transition: box-shadow 0.2s;
}

.center-card-area.my-turn {
  box-shadow: 0 0 0 3px #3b82f6;
  border-radius: 8px;
}

.card-back {
  width: 50px;
  height: 70px;
  background-color: #ffffff;
  border: 2px solid #cccccc;
  border-radius: 4px;
}

.player-nickname {
  margin-top: 5px;
  font-weight: bold;
  font-size: 0.9rem;
  text-align: center;
}

.turn-label {
  font-size: 0.75rem;
  color: #3b82f6;
  margin-left: 4px;
}

.bell-wrapper {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.chat-box-position {
  position: absolute;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  width: 420px;
  z-index: 1000;
}

.start-button {
  position: absolute;
  bottom: 100px;
  left: 50%;
  transform: translateX(-50%);
  padding: 0.6rem 1.2rem;
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: bold;
  cursor: pointer;
  z-index: 500;
}

.start-button[disabled] {
  background-color: #a5d6a7;
  cursor: not-allowed;
}

.start-button:hover:not([disabled]) {
  background-color: #45a049;
}
</style>
