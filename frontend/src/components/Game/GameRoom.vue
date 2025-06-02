<template>
  <div class="game-room">
    <ScoreBoard :players="players" :currentUserId="currentUserId" />

    <div class="main-area">
      <div
        v-for="(player, index) in players"
        :key="player.id"
        class="center-card-area"
        :style="getPlayerCardStyle(index, players.length)"
      >
        <PlayerCard
          v-if="player.latestCard"
          :card="player.latestCard"
          :isCurrentTurn="player.id === currentUserId"
        />
        <div class="player-nickname">{{ player.nickname }}</div>
      </div>

      <div class="bell-wrapper">
        <BellButton @ring="ringBell" />
      </div>
    </div>

    <ChatBox
      :messages="messages"
      v-model:modelValue="chatInput"
      @send="sendMessage"
      class="chat-box-position"
    />
  </div>
</template>

<script>
import PlayerCard from "./PlayerCard.vue";
import BellButton from "./BellButton.vue";
import ChatBox from "./ChatBox.vue";
import ScoreBoard from "./ScoreBoard.vue";

export default {
  name: "GameRoom",
  components: { PlayerCard, BellButton, ChatBox, ScoreBoard },

  data() {
    return {
      players: [
        { id: "1", nickname: "유저1", remainingCards: 5, latestCard: { fruit: "🍓", count: 3 } },
        { id: "2", nickname: "유저2", remainingCards: 4, latestCard: { fruit: "🥝", count: 1 } },
        { id: "3", nickname: "유저3", remainingCards: 6, latestCard: { fruit: "🍌", count: 2 } },
        { id: "4", nickname: "유저4", remainingCards: 1, latestCard: { fruit: "🍇", count: 4 } },
        { id: "5", nickname: "유저5", remainingCards: 3, latestCard: { fruit: "🍓", count: 5 } },
        { id: "6", nickname: "유저6", remainingCards: 2, latestCard: { fruit: "🥝", count: 2 } },
      ],
      currentUserId: "1",
      messages: [],
      chatInput: "",
    };
  },

  methods: {
    getPlayerCardStyle(index, total) {
      const angle = (360 / total) * index - 90;
      const radius = 150;
      const rad = (angle * Math.PI) / 180;
      const x = radius * Math.cos(rad);
      const y = radius * Math.sin(rad);
      return {
        top: `calc(50% + ${y}px)`,
        left: `calc(50% + ${x}px)`,
        transform: "translate(-50%, -50%)",
        position: "absolute",
      };
    },

    ringBell() {
      alert("종을 쳤습니다!");
    },

    sendMessage() {
      if (!this.chatInput.trim()) return;
      this.messages.push({
        id: Date.now(),
        nickname: this.players.find(p => p.id === this.currentUserId)?.nickname || "익명",
        text: this.chatInput,
      });
      this.chatInput = "";
    },
  },
};
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

.main-area {
  position: relative;
  width: 80vw;
  max-width: 700px;
  height: 80vw;
  max-height: 700px;
  margin: 20px 0 10px;
  border-radius: 50%;
}

.center-card-area {
  width: 100px;
  height: 200px; /* 닉네임 공간 확보 */
  cursor: pointer;
  position: absolute;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
}

.player-nickname {
  margin-top: 5px;
  font-weight: bold;
  font-size: 0.9rem;
  text-align: center;
  user-select: text;
}

.bell-wrapper {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.chat-box-position {
  width: 420px;
  margin-top: 15px;
}
</style>
