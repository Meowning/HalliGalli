<template>
  <div class="score-board">
    <div
      v-for="player in players"
      :key="player.id"
      :class="['score-item', { 'current-player': player.id === currentUserId }]"
    >
      {{ player.nickname }} ({{ player.remainingCards }}장)
    </div>
  </div>
</template>

<script>
export default {
  name: "ScoreBoard",
  props: {
    players: Array,
    currentUserId: String,
  },
};
</script>

<style scoped>
.score-board {
  display: flex;
  gap: 15px;
  margin-bottom: 10px;
  justify-content: center;
  font-weight: bold;
  user-select: none;
}

.score-item {
  padding: 5px 10px;
  border-radius: 5px;
  background: #d9e8ff;
  color: #333;
  cursor: default;
}

.current-player {
  background: #3680ff;
  color: white;
}
</style>
