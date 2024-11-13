<script lang="ts">
export default {
  data() {
    return {
      currentPage: 1,
      pageSize: 10,
      total: 0,
      modelData: []
    };
  },
  methods: {
    // 处理分页变化
    handlePageChange(page: number) {
      this.currentPage = page;
      this.loadModelData();
    },
    // 加载模型数据
    async loadModelData() {
      try {
        const response = await this.$axios.get('/api/models');
        if (response.data.result === 0) {
          this.total = response.data.models.length;
          this.modelData = response.data.models;
        } else {
          this.$message.error('获取模型数据失败');
        }
      } catch (error) {
        this.$message.error('获取模型数据出错');
      }
    },
  },
  mounted() {
    this.loadModelData();
  }
};
</script>

<template>
  <el-container>
    <!-- 主体内容 -->
    <el-main>
      <!-- 表格展示模型信息 -->
      <el-table :data="modelData">
        <el-table-column prop="module_id" label="模型ID"></el-table-column>
        <el-table-column prop="name" label="模型名称"></el-table-column>
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