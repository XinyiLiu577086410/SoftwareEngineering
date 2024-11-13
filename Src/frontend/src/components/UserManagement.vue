<script lang="ts">
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
    async handleDelete(row: any) {
      try {
        // 弹出确认删除提示框
        await this.$confirm(`确认删除用户 ${row.username} 吗？`, '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        });
        // 发起删除请求
        const response = await this.$axios.get('/api/delete', {
          params: { username: row.username } // 传递需要删除的用户名作为参数
        });
        // 根据返回的结果判断是否删除成功
        if (response.data.status === 0 && response.data.result === 0) {
          // 删除成功，提示并刷新数据
          this.$message.success(`用户 ${row.username} 已删除`);
          this.loadUserData();
        } else if (response.data.result === -5) {
          this.$message.error(`用户 ${row.username} 不存在`);
        } else if (response.data.result === -4) {
          this.$message.error('用户名参数缺失');
        } else if (response.data.result === -3) {
          this.$message.error('权限不足');
        } else if (response.data.result === -2) {
          this.$message.error('登录的用户不存在');
        } else {
          this.$message.error('用户未登录');
        }
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
        const response = await this.$axios.get('/api/users');
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
    },
  },
  mounted() {
    this.loadUserData();
  }
};
</script>

<template>
    <el-container>
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
</template>
  
<style scoped>

.el-pagination {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}
</style>