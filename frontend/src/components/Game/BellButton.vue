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
  width: 80px;
  height: 80px;

  display: flex;
  align-items: center;
  justify-content: center;

  font-size: 2.5rem;

  border-radius: 50%;
  background: #ffd633;
  border: 3px solid #ccaa00;
  box-shadow: 0 0 10px rgba(204, 170, 0, 0.7);

  cursor: pointer;
  user-select: none;
  outline: none;

  transition: background 0.2s, box-shadow 0.2s;
}

.bell-button:hover {
  background: #ffec66;
  box-shadow: 0 0 12px rgba(204, 170, 0, 0.9);
}
</style>
