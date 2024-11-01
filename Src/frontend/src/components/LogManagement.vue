<script lang="ts">
export default {
  data() {
    return {
      currentPage: 1,
      pageSize: 10,
      total: 0,
      chatData: [],
      historyData: []
    };
  },
  methods: {
    // 处理分页变化
    handlePageChange(page: number) {
      this.currentPage = page;
      this.loadHistoryData();
    },
    async loadHistoryData() {
      try {
        const response = await this.$axios.get('/api/histories');
        if (response.data.result === 0) {
          // 处理分页
          const start = (this.currentPage - 1) * this.pageSize;
          const end = this.currentPage * this.pageSize;
          // 更新数据
          this.total = response.data.history.length;
          this.chatData = response.data.chat.slice(start, end);
          this.historyData = response.data.history.slice(start, end);
        } else if (response.data.result === -3) {
          this.$message.error('权限不足');
        } else {
          this.$message.error('获取数据失败');
        }
      } catch (error) {
        this.$message.error('获取数据出错');
        console.error('Error fetching history data:', error);
      }
    }
  },
  mounted() {
    this.loadHistoryData();
  }
};
</script>

<template>
  <el-container>
    <el-main>
      <el-tabs>
        <el-tab-pane label="聊天记录">
          <el-table :data="chatData">
            <el-table-column prop="username" label="用户名"></el-table-column>
            <el-table-column prop="module_id" label="模块ID"></el-table-column>
            <el-table-column prop="prompt" label="提示内容"></el-table-column>
            <el-table-column prop="date" label="日期"></el-table-column>
          </el-table>
        </el-tab-pane>

        <el-tab-pane label="历史记录">
          <el-table :data="historyData">
            <el-table-column prop="username" label="用户名"></el-table-column>
            <el-table-column prop="amount" label="金额"></el-table-column>
            <el-table-column prop="date" label="日期"></el-table-column>
          </el-table>
        </el-tab-pane>
      </el-tabs>

      <!-- 分页 -->
      <el-pagination
        background
        layout="prev, pager, next"
        :total="total"
        :current-page="currentPage"
        :page-size="pageSize"
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