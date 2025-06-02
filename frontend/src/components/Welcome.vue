<template>
  <div class="container">
    <h2>🔔 할리갈리 온라인 🍎</h2>
    <div>
      <p>인게임 닉네임을 입력해주세요.</p>
      <input v-model="nickname" type="text" placeholder="닉네임" />
      <button @click="enterLobby">입장하기!</button>
    </div>
  </div>
</template>

<script>
export default {
  name: "NicknameForm",
  data() {
    return {
      nickname: "",
    };
  },
  methods: {
    enterLobby() {
      if (!this.nickname.trim()) {
        alert("닉네임을 입력하세요");
        return;
      }
      localStorage.setItem("nickname", this.nickname);
      this.$router.push("/lobby");
    },
  },
};
</script>
