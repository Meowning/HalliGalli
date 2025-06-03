<!-- frontend/src/components/NicknameForm.vue -->
<template>
  <div class="container">
    <h2>🔔 할리갈리 온라인 🍓</h2>
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
    async enterLobby() {
      if (!this.nickname.trim()) {
        alert("닉네임을 입력하세요");
        return;
      }

      const formData = new URLSearchParams();
      formData.append("nickname", this.nickname.trim());

      try {
        const res = await fetch("/api/enter_nickname", {
          method: "POST",
          headers: { "Content-Type": "application/x-www-form-urlencoded" },
          body: formData,
          credentials: "include",
        });

        if (!res.ok) {
          const text = await res.text();
          alert("닉네임 설정 실패: " + text);
          return;
        }

        this.$router.push("/lobby");
      } catch (err) {
        console.error(err);
        alert("서버 통신 오류");
      }
    },
  },
};
</script>
