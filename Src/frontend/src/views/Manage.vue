<script lang="ts">
import UserManagement from '@/components/UserManagement.vue';
import ModelManagement from '@/components/ModelManagement.vue';
import ClusterManagement from '@/components/ClusterManagement.vue';
import LogManagement from '@/components/LogManagement.vue';

export default {
  data() {
    return {
      currentComponent: 'UserManagement', // 默认显示的组件
    };
  },
  methods: {
    // 处理菜单选择
    handleMenuSelect(index) {
      switch (index) {
        case '1':
          this.currentComponent = 'UserManagement';
          break;
        case '2':
          this.currentComponent = 'ModelManagement';
          break;
        case '3':
          this.currentComponent = 'ClusterManagement';
          break;
        case '4':
          this.currentComponent = 'LogManagement';
          break;
      }
    },
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
    },
  },
  components: {
    UserManagement,
    ModelManagement,
    ClusterManagement,
    LogManagement,
  },
};
</script>

<template>
  <div style="display: flex" class="full">
    <el-aside>
      <!-- 菜单 -->
      <el-menu default-active="1" @select="handleMenuSelect">
        <el-menu-item index="1">
          <el-icon><user /></el-icon>
          <span>用户管理</span>
        </el-menu-item>
        <el-menu-item index="2">
          <el-icon><goods /></el-icon>
          <span>模型管理</span>
        </el-menu-item>
        <el-menu-item index="3">
          <el-icon><opportunity /></el-icon>
          <span>集群管理</span>
        </el-menu-item>
        <el-menu-item index="4">
          <el-icon><message /></el-icon>
          <span>日志管理</span>
        </el-menu-item>
      </el-menu>
      <!-- 用户中心及登出按钮 -->
      <el-card class="card">
        <el-button @click="$router.push('/user')">用户中心</el-button>
        <el-button @click="handleLogout">登出</el-button>
      </el-card>
    </el-aside>
    <el-main>
      <div style="flex-grow: 1">
        <!-- 动态组件 -->
        <component :is="currentComponent" />
      </div>
    </el-main>
  </div>
</template>

<style scoped>

</style>