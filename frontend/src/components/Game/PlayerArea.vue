<template>
  <div class="player-card" :class="{ 'current-turn': isCurrentTurn }">
    <div class="card">
      <div class="fruit">{{ card.fruit }}</div>
      <div class="count">{{ card.count }}</div>
    </div>
    <div class="nickname">{{ nickname }}</div>
  </div>
</template>

<script>
export default {
  name: "PlayerCard",
  props: {
    card: Object,
    isCurrentTurn: Boolean,
    nickname: String
  },
};
</script>

<style scoped>
.player-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin: 0 5px;
}

.card {
  width: 60px;
  height: 90px;
  background: white;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.15);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  font-size: 2rem;
  cursor: pointer;
  position: relative;
}

.card .fruit {
  font-size: 2.5rem;
}

.card .count {
  font-size: 1rem;
  color: #555;
  position: absolute;
  bottom: 6px;
  right: 6px;
}

.current-turn .card {
  border: 3px solid #3b82f6;
  box-shadow: 0 0 8px #3b82f6;
}

.nickname {
  margin-top: 6px;
  font-weight: bold;
  color: #444;
  font-size: 0.9rem;
  user-select: none;
}
</style>
