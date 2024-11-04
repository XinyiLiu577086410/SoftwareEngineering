<script lang="ts">
import { computed, ref } from 'vue';
import * as echarts from 'echarts';
import { useloginStatus } from '@/stores/loginStatus';

export default {
  data() {
    return {
      loginStatus : computed(() => useloginStatus()),
      balance: ref(0),          // 当前余额
      redeemCode: ref(''),       // 充值兑换码
      chart: null as HTMLElement | null // 图表 DOM 引用
    };
  },
  methods: {
    // 兑换余额功能
    async redeemBalance() {
      if (this.redeemCode) {
        try {
            console.log(this.redeemCode)
            const response = await this.$axios.get('/api/fund', {
              params:{
                code: this.redeemCode,
              }
            });
            console.log(response.data)
            if (response.data.result === 0) {
              this.$message.success('充值成功');
              this.balance = response.data.balance;
              this.redeemCode = ''; // 清空输入框
            } else {
              this.$message.error('充值失败');
            }
          } catch (error) {
            // 处理请求错误
            console.error(error);
            this.$message.error('充值请求失败，请稍后重试');
          }
      }
    },
    async loadUserInfo() {
      try {
        const response = await this.$axios.get('/api/info');
        if (response.data.result === 0) {
          this.balance = response.data.balance;
          this.loginStatus.setManager(response.data.manager);
        } else {
          this.$message.error('用户信息获取失败');
        }
      } catch (error) {
        // 处理请求错误
        console.error(error);
        this.$message.error('用户信息获取出错，请稍后重试');
      }
    },
    // 初始化图表
    async initChart() {
      try {
        const response = await this.$axios.get('/api/consumption');
        if (response.data.result === 0) {
          const { months, values } = response.data.consumption;
          // 使用 ECharts 显示数据
          if (this.chart) {
            const chartInstance = echarts.init(this.chart);
            const option = {
              xAxis: {
                type: 'category',
                data: months.map((month: any) => `${month}月`), // 处理月份名称
              },
              yAxis: {
                type: 'value'
              },
              series: [
                {
                  data: values.map((value: number) => Math.abs(value)), // 将消费金额转为正数
                  type: 'line',
                  smooth: true, // 平滑曲线
                }
              ]
            };
            chartInstance.setOption(option);
          }
        } else {
          this.$message.error('获取消费数据失败');
        }
      } catch (error) {
        console.error(error);
        this.$message.error('请求出错，请稍后重试');
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
    }
  },
  mounted() {
    // 等页面挂载完成后初始化图表
    this.chart = this.$refs.chart as HTMLElement;
    this.initChart();
    this.loadUserInfo();
  }
};
</script>

<template>
  <div class="full">
    <el-container>
      <!-- 左侧菜单栏 -->
      <el-aside>
        <el-menu>
          <el-menu-item index="1">
            <el-icon><location/></el-icon>
            <span>个人管理</span>
          </el-menu-item>
          <el-menu-item index="2" @click="$router.push('/manage')">
            <el-icon><setting/></el-icon>
            <span>用户管理</span>
          </el-menu-item>
        </el-menu>
        <el-card class="card">
          <div style="display: flex; align-items: center; gap: 10px;">
              <el-button @click="$router.push('/')">首页</el-button>
            <div v-if="loginStatus.isLoggedIn">
              <el-button @click="handleLogout">登出</el-button>
            </div>
          </div>
        </el-card>
      </el-aside>

      <!-- 右侧内容区域 -->
      <el-main>
        <div class="content">
          <el-card class="balance-card">
            <!-- 消费历史统计图表 -->
            <div slot="header" class="clearfix">
              每月费用统计/元
            </div>
            <div ref="chart" class="chart"></div>

          <!-- 余额显示及充值 -->
            <div class="balance">
              <span>当前余额</span>
              <h2>{{ balance }} 元</h2>
            </div>
            <el-input v-model="redeemCode" placeholder="输入兑换码">
              <template #prefix>
                <el-icon><location/></el-icon>
              </template>
            </el-input>
            <el-button type="primary" @click="redeemBalance">兑换余额</el-button>
          </el-card>
        </div>
      </el-main>
    </el-container>
  </div>
</template>

<style scoped>

.content {
  display: flex;
  justify-content:center;
}

.chart {
  height: 600px;
  width: 100%;
}

.balance-card {
  height: 100%;
  width: 100%;
  text-align: center;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.balance {
  margin-bottom: 20px;
}

</style>