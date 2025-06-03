<template>
  <div class="container">
    <h2>🔔 할리갈리 온라인 🍓</h2>

    <div>
      <h3>방 목록</h3>
      <div id="room-list">
        <div
          v-for="room in rooms"
          :key="room.roomId"
          class="room"
          @click="goToGameRoom(room.roomId)"
        >
          {{ room.roomId }} (현재 {{ room.currentPlayers }}명)
        </div>
        <div v-if="rooms.length === 0" class="no-rooms">
          현재 열린 방이 없습니다.
        </div>
      </div>

      <h4>또는 새 방 만들기</h4>
      <input
        v-model="newRoomName"
        type="text"
        placeholder="방 이름 (표시용)"
      />

      <div style="display: flex; align-items: center; margin: 0.75rem 0;">
        <label
          style="margin-right: 1rem; display: flex; align-items: center; white-space: nowrap;"
        >
          <input
            type="checkbox"
            v-model="isPrivate"
            style="margin-right: 0.4rem;"
            @change="togglePasswordInput"
          />
          비밀방
        </label>
        <input
          type="password"
          v-model="roomPassword"
          placeholder="비밀번호 (선택)"
          style="flex: 1;"
          :disabled="!isPrivate"
        />
      </div>
      <p>할리갈리는 최소 2명부터 플레이 가능합니다.</p>
      <button @click="createRoom">방 만들기</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from "vue";
import { io } from "socket.io-client";
import { useRouter } from "vue-router";

const router = useRouter();
const socket = ref(null);
const rooms = ref([]);
const newRoomName = ref("");
const isPrivate = ref(false);
const roomPassword = ref("");

const BACKEND_HOST = import.meta.env.VITE_BACKEND_HOST || window.location.hostname;
const BACKEND_PORT = import.meta.env.VITE_BACKEND_PORT || "5000";
const BACKEND_URL = `http://${BACKEND_HOST}:${BACKEND_PORT}`;

function togglePasswordInput() {
  if (!isPrivate.value) {
    roomPassword.value = "";
  }
}

function fetchRoomList() {
  socket.value.emit("room/list");
}

function createRoom() {
  if (!newRoomName.value.trim()) {
    alert("방 이름을 입력하세요");
    return;
  }
  const payload = {
    name: newRoomName.value.trim(),
    ...(isPrivate.value ? { password: roomPassword.value } : {}),
  };
  socket.value.emit("room/create", payload);

  newRoomName.value = "";
  isPrivate.value = false;
  roomPassword.value = "";
}

function goToGameRoom(roomId) {
  router.push({ name: "GameRoom", params: { roomId } });
}

onMounted(() => {
  socket.value = io(BACKEND_URL, {
    path: "/socket.io",
    transports: ["websocket"],
    withCredentials: true,
  });

  socket.value.on("connect", () => {
    console.log("[Lobby] Socket connected to", BACKEND_URL);
    fetchRoomList();
  });

  socket.value.on("disconnect", () => {
    console.log("[Lobby] Socket disconnected");
  });

  socket.value.on("room/list", (roomList) => {
    rooms.value = roomList.map((r) => {
      return {
        roomId: r.roomId,
        currentPlayers: r.playerCount,
      };
    });
  });

  socket.value.on("room/create/success", (data) => {
    console.log("[Lobby] room/create/success:", data);
    router.push({ name: "GameRoom", params: { roomId: data.roomId } });
  });

  socket.value.on("room/error", (e) => {
    console.warn("[Lobby] room/error:", e);
    alert(e.msg || "방 입장 중 오류가 발생했습니다.");
  });
});

onBeforeUnmount(() => {
  if (socket.value) {
    socket.value.disconnect();
  }
});
</script>

<style scoped>
.container {
  max-width: 600px;
  margin: 2rem auto;
  padding: 1rem;
  border: 1px solid #ddd;
  border-radius: 8px;
}

#room-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.room {
  padding: 0.75rem;
  background-color: #f5f5f5;
  border-radius: 4px;
  cursor: pointer;
  user-select: none;
  transition: background-color 0.2s;
}

.room:hover {
  background-color: #e0e0e0;
}

.no-rooms {
  color: #888;
  font-style: italic;
}
</style>
