<template>
  <div class="player-card" :class="{ 'current-turn': isCurrentTurn }">
    <div class="fruit-grid">
      <div
        v-for="(fruit, idx) in fruitList"
        :key="idx"
        class="fruit-emoji"
        :style="getFruitStyle(idx)"
      >
        {{ card.fruit }}
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
      const count = Math.min(this.card.count, 5);
      return Array(count).fill(this.card.fruit);
    },
  },
  methods: {
    getFruitStyle(index) {
      if (this.card.count === 1) {
        return { left: "50%", top: "50%" };
      }
      if (this.card.count === 2) {
        const twoPos = [
          { left: "30%", top: "30%" },
          { left: "70%", top: "70%" }
        ];
        return twoPos[index];
      }
      if (this.card.count === 3) {
        const threePos = [
          { left: "30%", top: "30%" },
          { left: "50%", top: "50%" },
          { left: "70%", top: "70%" }
        ];
        return threePos[index];
      }
      if (this.card.count === 4) {
        const fourPos = [
          { left: "25%", top: "25%" },
          { left: "75%", top: "25%" },
          { left: "25%", top: "75%" },
          { left: "75%", top: "75%" }
        ];
        return fourPos[index];
      }
      if (this.card.count >= 5) {
        const fivePos = [
          { left: "25%", top: "25%" },
          { left: "75%", top: "25%" },
          { left: "50%", top: "50%" },
          { left: "25%", top: "75%" },
          { left: "75%", top: "75%" }
        ];
        return fivePos[index];
      }

      return { left: "50%", top: "50%" };
    },
  },
};
</script>

<style scoped>
.player-card {
  position: relative;
  width: 70px;
  height: 140px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 0 5px rgba(0, 0, 0, 0.15);
  padding: 6px;
  user-select: none;
  transition: border-color 0.3s ease, box-shadow 0.3s ease;
}

.current-turn {
  border: 2px solid #3b82f6;
  box-shadow: 0 0 12px #3b82f6;
}

.fruit-grid {
  position: relative;
  width: 100%;
  height: 100%;
}

.fruit-emoji {
  position: absolute;
  transform: translate(-50%, -50%);
  font-size: 1.5rem;
  line-height: 1;
  user-select: none;
}
</style>
