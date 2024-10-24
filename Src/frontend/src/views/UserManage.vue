<script lang="ts">
import axios from 'axios';
import { defineComponent, ref } from 'vue';
import { ElMessage, ElMessageBox } from 'element-plus';

export default defineComponent({
  data() {
    return {
      currentPage: 1, // 当前页码
      total: 2, // 数据总数
      userData: [
        { username: 'John', group: 'User', balance: '10.00' },
        { username: 'Alex', group: 'User', balance: '5.00' },
      ]
      // userData: [] as Array<any>
    };
  },
  methods: {
    // 处理编辑操作
    handleEdit(row: any) {
      ElMessage({
        message: `管理用户: ${row.username}`,
        type: 'success'
      });
    },
    // 处理删除操作
    handleDelete(row: any) {
      ElMessageBox.confirm(
        `确认删除用户 ${row.username} 吗？`,
        '提示',
        {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }
      )
        .then(() => {
          ElMessage({
            type: 'success',
            message: `用户 ${row.username} 已删除`
          });
        })
        .catch(() => {
          ElMessage({
            type: 'info',
            message: '删除已取消'
          });
        });
    },
    // 处理分页变化
    handlePageChange(page: number) {
      this.currentPage = page;
      // 模拟分页数据请求
      this.loadUserData();
    },
    // 模拟加载用户数据
    // 请求用户数据
    async loadUserData() {
      try {
          const response = await axios.get('https://api.example.com/users', {
          params: {
              page: this.currentPage, // 请求的页码
              pageSize: 10 // 每页显示的数据数量
          }
          });
          // 更新用户数据和总条目数
          this.userData = response.data.users;
          this.total = response.data.total; // 假设后端返回了总数据量
      } catch (error) {
          ElMessage({
          message: '获取用户数据失败，请稍后重试',
          type: 'error'
          });
          console.error('Error fetching user data:', error);
      }
    }
  },
  // mounted() {
  //   // 组件挂载时加载第一页的数据
  //   this.loadUserData();
  // }
});
</script>

<template>
  <div class="full">
    <!-- 侧边栏 -->
    <el-container>
      <el-aside>
        <el-menu default-active="1">
          <el-menu-item index="1">
            <el-icon><user/></el-icon>
            <span>用户管理</span>
          </el-menu-item>
          <el-menu-item index="2">
            <el-icon><goods/></el-icon>
            <span>模型管理</span>
          </el-menu-item>
          <el-menu-item index="3">
            <el-icon><opportunity/></el-icon>
            <span>集群管理</span>
          </el-menu-item>
          <el-menu-item index="4">
            <el-icon><message/></el-icon>
            <span>日志管理</span>
          </el-menu-item>
        </el-menu>
        <el-card class="card">
          <router-link to="/user">
            <!-- 用户中心 -->
            <el-button>用户中心</el-button>
          </router-link>
          <!-- 登出按钮 -->
          <el-button>登出</el-button>
        </el-card>
      </el-aside>

      <!-- 主体内容 -->
      <el-main>
        <!-- 表格展示用户信息 -->
        <el-table :data="userData">
          <el-table-column prop="username" label="用户名"></el-table-column>
          <el-table-column prop="group" label="群组"></el-table-column>
          <el-table-column prop="balance" label="余额"></el-table-column>
          <el-table-column label="操作">
            <template #default="scope">
              <el-button @click="handleEdit(scope.row)" type="primary">管理</el-button>
              <el-button @click="handleDelete(scope.row)" type="primary" style="color: red;">删除</el-button>
            </template>
          </el-table-column>
        </el-table>

        <!-- 分页 -->
        <el-pagination
          background
          layout="prev, pager, next"
          :total="total"
          :current-page="currentPage"
          @current-change="handlePageChange">
        </el-pagination>
      </el-main>
    </el-container>
  </div>
</template>
  
<style scoped>
.user-management-container {
  padding: 20px;
}

.el-pagination {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}
</style>  