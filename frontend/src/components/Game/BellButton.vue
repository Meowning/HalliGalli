<template>
  <button class="bell-button" @click="$emit('ring')">
    🔔
  </button>
</template>

<script>
export default {
  name: "BellButton",
};
</script>

<style scoped>
.bell-button {
  font-size: 2.5rem;
  padding: 15px 30px;
  border-radius: 50%;
  background: #ffd633;
  border: 3px solid #ccaa00;
  box-shadow: 0 0 10px #ccaa00;
  cursor: pointer;
  user-select: none;
  outline: none;
}
.bell-button:hover {
  background: #ffec66;
}
</style>
