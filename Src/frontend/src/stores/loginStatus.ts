import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useloginStatus = defineStore('loginStatus', () => {
  const isLoggedIn = ref(false); // 登录状态
  const isManager = ref(false); // 管理员
  const username = ref('');      // 用户名

  function setLoginStatus(status: boolean) {
    isLoggedIn.value = status;
  }

  function setUsername(name: string) {
    username.value = name;
  }

  function setManager(m: boolean) {
    isManager.value = m;
  }

  function logout() {
    isLoggedIn.value = false;
    username.value = '';
    isManager.value = false;
  }

  return {
    isLoggedIn,
    username,
    isManager,
    setLoginStatus,
    setUsername,
    setManager,
    logout,
  };
});
