<script lang="ts">
import { RouterView } from 'vue-router'
import { computed, ref } from 'vue';
import { useloginStatus } from '@/stores/loginStatus';

export default {
  data () {
    return {
      loginStatus : computed(() => useloginStatus()),
      isCollapse : ref(false),
      circleUrl : ref('https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png'),
      input : ref(''),
    }
  },
  methods: {
    async handleLogout() {
      try {
        const response = await this.$axios.get('/api/logout');
        if (response.data.result === 0) {
          this.loginStatus.logout();
          this.$message.success('登出成功');
          this.$router.push('/');
        } else {
          this.$message.error('登出失败，请稍后重试');
        }
      } catch (error) {
        this.$message.error('请求出错，请稍后重试');
        console.error('Logout error:', error);
      }
    }
  }
}
</script>

<template>
  <div class="full">
    <el-container>
      <el-aside>
        <!-- 目录栏 -->
        <el-menu default-active="2" :collapse="isCollapse">
          <el-sub-menu index="1">
            <template #title>
              <el-icon><location/></el-icon>
              <span>Navigator One</span>
            </template>
            <el-menu-item-group>
              <template #title><span>Group One</span></template>
              <el-menu-item index="1-1">item one</el-menu-item>
              <el-menu-item index="1-2">item two</el-menu-item>
            </el-menu-item-group>
            <el-menu-item-group title="Group Two">
              <el-menu-item index="1-3">item three</el-menu-item>
            </el-menu-item-group>
            <el-sub-menu index="1-4">
              <template #title><span>item four</span></template>
              <el-menu-item index="1-4-1">item one</el-menu-item>
            </el-sub-menu>
          </el-sub-menu>
          <el-menu-item index="2">
            <el-icon><setting/></el-icon>
            <template #title>Navigator Two</template>
          </el-menu-item>
        </el-menu>
        <el-card class="card">
          <div style="display: flex; align-items: center; gap: 10px;">
            <!-- 头像 -->
            <el-avatar :size="50" :src="circleUrl" @click="$router.push('/user')"/>
            <div style="font-size: large">{{ loginStatus.username }}</div>
            <div v-if="loginStatus.isLoggedIn">
              <!-- 登出 -->
              <el-button @click="handleLogout">登出</el-button>
            </div>
            <div v-else>
              <!-- 登录 -->
              <el-button @click="$router.push('/login')">登录</el-button>
            </div>
          </div>
        </el-card>
      </el-aside>
      <el-main>
          <el-main style="height: 80%;">
          </el-main>
          <!-- 输入框 -->
          <el-input v-model="input" :autosize="{ minRows: 1, maxRows: 5 }" type="textarea" placeholder="Please input" clearable/>
      </el-main>
    </el-container>
  </div>
  <router-view></router-view>
</template>

<style scoped>

</style>