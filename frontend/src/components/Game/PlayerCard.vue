<template>
  <div :class="['player-card', { 'current-turn': isCurrentTurn }]">
    <div class="fruit-grid" :style="gridStyle">
      <div
        v-for="(fruit, idx) in fruitList"
        :key="idx"
        class="fruit-emoji"
      >
        {{ fruit }}
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "PlayerCard",
  props: {
    card: { type: Object, required: true },
    isCurrentTurn: { type: Boolean, default: false },
  },
  computed: {
    fruitList() {
      const count = Math.min(this.card.count, 9); // 최대 9개까지 표시
      return Array(count).fill(this.card.fruit);
    },
    gridStyle() {
      return {
        display: "grid",
        "grid-template-columns": "repeat(3, 1fr)",
        "grid-template-rows": "repeat(3, 1fr)",
        "justify-items": "center",
        "align-items": "center",
        gap: "6px",
        width: "100%",
        height: "100px",
      };
    },
  },
};
</script>

<style scoped>
.player-card {
  border: 2px solid transparent;
  border-radius: 8px;
  padding: 10px;
  background: white;
  box-shadow: 0 0 5px #aaa;
  transition: border-color 0.3s ease;
  width: 100px;
  height: 130px;
  user-select: none;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.current-turn {
  border-color: #36c;
  box-shadow: 0 0 15px #369;
}

.fruit-emoji {
  font-size: 1.7rem;
  line-height: 1;
}
</style>
