<template>
  <div class="fruit-card" @click="$emit('click')">
    <div
      v-for="n in card.count"
      :key="n"
      class="fruit"
    >
      {{ card.fruit }}
    </div>
  </div>
</template>

<script>
export default {
  name: "FruitCard",
  props: {
    card: {
      type: Object,
      required: true,
    },
  },
};
</script>

<style scoped>
.fruit-card {
  border: 1px solid #ccc;
  border-radius: 10px;
  width: 70px;
  height: 100px;
  background: white;
  box-shadow: 0 0 5px #aaa;
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  align-content: center;
  cursor: pointer;
  user-select: none;
}

.fruit {
  font-size: 2rem;
  margin: 2px;
  width: 28px;
  height: 28px;
  text-align: center;
  line-height: 28px;
  user-select: none;
}
</style>
