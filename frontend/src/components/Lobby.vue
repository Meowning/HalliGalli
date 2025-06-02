<template>
  <div class="container">
    <h2>🔔 할리갈리 온라인 🍎</h2>

    <div>
      <h3>방 목록</h3>
      <div id="room-list">
        <div
          v-for="room in rooms"
          :key="room.roomId"
          class="room"
          @click="joinRoom(room)"
        >
          {{ room.name }} ({{ room.current }}/{{ room.max }})
        </div>
      </div>

      <h4>또는 새 방 만들기</h4>
      <input v-model="newRoomName" type="text" placeholder="방 이름" />

      <div style="display: flex; align-items: center; margin: 0.75rem 0;">
        <label style="margin-right: 1rem; display: flex; align-items: center; white-space: nowrap;">
          <input type="checkbox" v-model="isPrivate" style="margin-right: 0.4rem;" @change="togglePasswordInput" />
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
      <p>할리갈리는 최소 2명, 최대 6명까지 플레이 가능합니다.</p>
      <button @click="createRoom">방 만들기</button>
    </div>
  </div>
</template>

<script>
export default {
  name: "Lobby",
  data() {
    return {
      rooms: [],
      newRoomName: "",
      isPrivate: false,
      roomPassword: "",
    };
  },
  created() {
    this.fetchRoomList();
  },
  methods: {
    fetchRoomList() {
      // 임시 테스트용 더미 데이터
      this.rooms = [
        { name: "같이할사람", roomId: "room1", current: 2, max: 4 },
        { name: "빨리시작", roomId: "room2", current: 1, max: 6 },
      ];
    },
    togglePasswordInput() {
      if (!this.isPrivate) {
        this.roomPassword = "";
      }
    },
    createRoom() {
      if (!this.newRoomName.trim()) {
        alert("방 이름을 입력하세요");
        return;
      }
      const visibility = this.isPrivate ? "비밀방" : "공개방";
      alert(`방 '${this.newRoomName}' (${visibility}, 비밀번호: ${this.roomPassword || "없음"}) 생성 요청됨 (구현 예정)`);
      // TODO: 서버에 방 생성 요청 보내기
    },
    joinRoom(room) {
      alert(`'${room.name}' 방 입장 (구현 예정)`);
      // TODO: 서버에 방 입장 요청 보내기
    },
  },
};
</script>