<script lang="ts">
import axios from 'axios';

export default {
  data() {
    return {
      currentPage: 1,
      pageSize: 10,
      total: 0,
      userData: []
    };
  },
  methods: {
    // 处理编辑操作
    handleEdit(row : any) {
      this.$message.success(`管理用户: ${row.username}`);
    },
    // 处理删除操作
    async handleDelete(row : any) {
      try {
        await this.$confirm(`确认删除用户 ${row.username} 吗？`, '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        });
        // 发起删除请求（示例代码中未实现具体删除操作）
        this.$message.success(`用户 ${row.username} 已删除`);
      } catch {
        this.$message.info('删除已取消');
      }
    },
    // 处理分页变化
    handlePageChange(page: number) {
      this.currentPage = page;
      this.loadUserData();
    },
    async loadUserData() {
      try {
        const response = await axios.get('/api/users');
        if (response.data.result === 0) {
          this.total = response.data.users.length;
          this.userData = response.data.users;
        } else {
          this.$message.error('获取用户数据失败，权限不足');
        }
      } catch (error) {
        this.$message.error('获取用户数据出错，请稍后重试');
        console.error('Error fetching user data:', error);
      }
    }
  },
  mounted() {
    this.loadUserData();
  }
};
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