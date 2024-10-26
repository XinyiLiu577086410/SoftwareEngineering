import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useloginStatus = defineStore('loginStatus', () => {
  const isLoggedIn = ref(false); // 登录状态
  const username = ref('');      // 用户名

  function setLoginStatus(status: boolean) {
    isLoggedIn.value = status;
  }

  function setUsername(name: string) {
    username.value = name;
  }

  function logout() {
    isLoggedIn.value = false;
    username.value = '';
  }

  return {
    isLoggedIn,
    username,
    setLoginStatus,
    setUsername,
    logout,
  };
});
