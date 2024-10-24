<script lang="ts">
import { ref, defineComponent } from 'vue';
import * as echarts from 'echarts';

export default defineComponent({
  data() {
    return {
      balance: ref(10),          // 当前余额
      redeemCode: ref(''),       // 充值兑换码
      chart: null as HTMLElement | null // 图表 DOM 引用
    };
  },
  methods: {
    // 兑换余额功能
    redeemBalance() {
      if (this.redeemCode) {
        this.balance += 10; // 模拟充值逻辑
        this.redeemCode = ''; // 清空输入框
      }
    },
    // 初始化图表
    initChart() {
      if (this.chart) {
        const chartInstance = echarts.init(this.chart);
        const option = {
          xAxis: {
            type: 'category',
            data: ['1月', '2月', '3月', '4月', '5月']
          },
          yAxis: {
            type: 'value'
          },
          series: [
            {
              data: [100, 150, 200, 50, 120],
              type: 'line'
            }
          ]
        };
        chartInstance.setOption(option);
      }
    }
  },
  mounted() {
    // 等页面挂载完成后初始化图表
    this.chart = this.$refs.chart as HTMLElement;
    this.initChart();
  }
});
</script>

<template>
  <div class="full">
    <el-container>
      <!-- 左侧菜单栏 -->
      <el-aside>
        <el-menu>
          <el-menu-item index="1">
            <i class="el-icon-user"></i>
            <span>个人信息管理</span>
          </el-menu-item>
        </el-menu>
        <div class="logout">
          <el-button>登出</el-button>
        </div>
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
                <el-icon-search />
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

.logout {
  position: absolute;
  bottom: 20px;
  left: 20px;
}
</style>