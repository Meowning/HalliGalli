<template>
  <div class="chat-box">
    <transition-group
      name="fade"
      tag="div"
      v-if="visibleMessages.length"
      ref="messagesContainer"
      class="messages"
      @scroll="onScroll"
    >
      <div
        v-for="msg in visibleMessages"
        :key="msg.id"
        class="message"
      >
        <strong>{{ msg.nickname }}:</strong> {{ msg.text }}
      </div>
    </transition-group>

    <div class="input-wrapper">
      <input
        type="text"
        :value="modelValueInput"
        @input="$emit('update:modelValue', $event.target.value)"
        @keyup.enter="$emit('send')"
        @focus="$emit('focusInput')"
        @blur="$emit('blurInput')"
        placeholder="채팅 입력 후 엔터"
        class="chat-input"
      />
    </div>
  </div>
</template>

<script>
export default {
  name: "ChatBox",
  props: {
    messages: {
      type: Array,
      required: true,
    },
    modelValue: {
      type: String,
      default: "",
    },
  },
  data() {
    return {
      modelValueInput: "",
      isUserScrolling: false,
    };
  },
  computed: {
    visibleMessages() {
      return this.messages;
    },
  },
  watch: {
    visibleMessages() {
      this.$nextTick(() => {
        if (!this.isUserScrolling) {
          this.scrollToBottom();
        }
      });
    },
    modelValue(val) {
      this.modelValueInput = val;
    },
  },
  mounted() {
    if (this.visibleMessages.length) {
      this.scrollToBottom();
    }
  },
  methods: {
    scrollToBottom() {
      const container = this.$refs.messagesContainer;
      if (container) {
        container.scrollTop = container.scrollHeight;
      }
    },
    onScroll() {
      const container = this.$refs.messagesContainer;
      if (!container) return;
      const isAtBottom =
        Math.abs((container.scrollHeight - container.clientHeight) -
                 container.scrollTop) < 10;
      this.isUserScrolling = !isAtBottom;
    },
  },
};
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s;
}
.fade-enter-from {
  opacity: 0;
}
.fade-leave-to {
  opacity: 0;
}

.chat-box {
  position: relative;
  width: 420px;
  min-height: 48px;
}

.messages {
  position: absolute;
  bottom: 48px;
  left: 0;
  right: 0;
  max-height: 180px;
  overflow-y: auto;
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(5px);
  border: 1px solid rgba(200, 200, 200, 0.4);
  border-radius: 6px;
  padding: 10px;
  box-sizing: border-box;
  text-align: left;
}

.message {
  margin-bottom: 8px;
  opacity: 0.8;
  font-size: 0.9rem;
  line-height: 1.3;
}

.input-wrapper {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 48px;
  padding: 6px 10px;
  background: rgba(255, 255, 255, 0.4);
  backdrop-filter: blur(5px);
  border-top: 1px solid rgba(200, 200, 200, 0.4);
  box-sizing: border-box;
  border-bottom-left-radius: 6px;
  border-bottom-right-radius: 6px;
}

.chat-input {
  width: 100%;
  height: 100%;
  border: 1px solid rgba(150, 150, 150, 0.5);
  border-radius: 4px;
  padding: 0 8px;
  font-size: 1rem;
  box-sizing: border-box;
  outline: none;
  background: rgba(255, 255, 255, 0.6);
  transition: background 0.2s, border-color 0.2s;
}

.chat-input:focus {
  background: rgba(255, 255, 255, 0.8);
  border-color: rgba(100, 100, 240, 0.7);
}
</style>
