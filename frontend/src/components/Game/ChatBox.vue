<template>
  <div class="chat-box">
    <div class="messages">
      <div v-for="msg in modelValue" :key="msg.id" class="message">
        <strong>{{ msg.nickname }}:</strong> {{ msg.text }}
      </div>
    </div>
    <input
      type="text"
      :value="modelValueInput"
      @input="$emit('update:modelValue', $event.target.value)"
      @keyup.enter="$emit('send')"
      placeholder="채팅 입력 후 엔터"
      class="chat-input"
    />
  </div>
</template>

<script>
export default {
  name: "ChatBox",
  props: {
    modelValue: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
      modelValueInput: "",
    };
  },
  watch: {
    modelValue(val) {
      this.modelValueInput = "";
    },
  },
};
</script>

<style scoped>
.chat-box {
  width: 100%;
  max-width: 420px;
  background: white;
  border: 1px solid #ccc;
  border-radius: 6px;
  display: flex;
  flex-direction: column;
  height: 200px;
}

.messages {
  flex-grow: 1;
  padding: 10px;
  overflow-y: auto;
  font-size: 0.9rem;
  line-height: 1.3;
}

.message {
  margin-bottom: 8px;
}

.chat-input {
  border: none;
  border-top: 1px solid #ddd;
  padding: 10px;
  font-size: 1rem;
  box-sizing: border-box;
  outline: none;
}
</style>
