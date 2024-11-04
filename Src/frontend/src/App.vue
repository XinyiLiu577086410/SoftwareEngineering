<script lang="ts">
import { RouterView } from 'vue-router'
import { computed } from 'vue';
import { useloginStatus } from '@/stores/loginStatus';
import { dayjs } from 'element-plus';

export default {
  data () {
    return {
      loginStatus : computed(() => useloginStatus()),
      isCollapse : false,
      circleUrl : 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png',
      input : '',
      module_id : 0,
      chatHistory: [] as Array<any>,
      chatDataToday : [] as Array<any>,
      chatDataLast3Days : [] as Array<any>,
      chatDataThisWeek : [] as Array<any>,
      chatDataThisMonth : [] as Array<any>,
      chatDataOlder : [] as Array<any>,
    }
  },
  methods: {
    async loadChatHistory() {
      try {
        this.chatDataToday = [];
        this.chatDataLast3Days = [];
        this.chatDataThisWeek = [];
        this.chatDataThisMonth = [];
        this.chatDataOlder = [];

        const response = await this.$axios.get('/api/chat_history');
        if (response.data.result === 0) {
          const chatData = response.data.chat;
          // 获取今天、近三天、本周和本月的时间范围
          const now = dayjs();
          const startOfToday = now.startOf('day');
          const startOfLast3Days = now.subtract(3, 'day').startOf('day');
          const startOfWeek = now.startOf('week');
          const startOfMonth = now.startOf('month');

          // 按时间范围分类
          chatData.forEach((chat : any) => {
            const chatDate = dayjs(chat.date);
            if (chatDate.isAfter(startOfToday)) {
              this.chatDataToday.push(chat);
            } else if (chatDate.isAfter(startOfLast3Days)) {
              this.chatDataLast3Days.push(chat);
            } else if (chatDate.isAfter(startOfWeek)) {
              this.chatDataThisWeek.push(chat);
            } else if (chatDate.isAfter(startOfMonth)) {
              this.chatDataThisMonth.push(chat);
            } else {
              this.chatDataOlder.push(chat); // 超过一个月之前的记录
            }
          });
        } else {
          console.error('获取聊天记录失败');
        }
      } catch (error) {
        console.error('加载聊天记录出错', error);
      }
    },
    async handleSubmit() {
      if (this.input.trim()) {
        this.chatHistory.push({ type: 'user', content: this.input });
        try {
          const response = await this.$axios.post('/api/chat', { module_id : this.module_id, prompt: this.input });
          if (response.data.status === 0 && response.data.result === 0) {
            this.chatHistory.push({
              type: 'bot',
              content: { picture: response.data.picture || null },
            });
          } else if (response.data.result === -1) {
            this.chatHistory.push({ type: 'bot', content: { picture: null, message: "Please log in." } });
          } else if (response.data.result === -2) {
            this.chatHistory.push({ type: 'bot', content: { picture: null, message: "Insufficient balance." } });
          }
        } catch (error) {
          console.error("Error with chat API:", error);
        }
        this.input = '';
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
    this.loadChatHistory();
  }
}
</script>

<template>
  <div class="full">
    <el-container>
      <el-aside>
        <!-- 目录栏 -->
        <el-menu default-active="1" :collapse="isCollapse">
          <el-sub-menu index="1-1" @click="loadChatHistory">
            <template #title><span>聊天记录</span></template>
            <!-- 今天的记录 -->
            <el-menu-item-group>
              <template #title><span>今天</span></template>
              <el-menu-item v-for="(chat, index) in chatDataToday" :key="'today-' + index">
                {{ chat.prompt }}
              </el-menu-item>
            </el-menu-item-group>
            <!-- 近三天的记录 -->
            <el-menu-item-group>
              <template #title><span>近三天</span></template>
              <el-menu-item v-for="(chat, index) in chatDataLast3Days" :key="'last3days-' + index">
                {{ chat.prompt }}
              </el-menu-item>
            </el-menu-item-group>
            <!-- 本周的记录 -->
            <el-menu-item-group>
              <template #title><span>本周</span></template>
              <el-menu-item v-for="(chat, index) in chatDataThisWeek" :key="'thisweek-' + index">
                {{ chat.prompt }}
              </el-menu-item>
            </el-menu-item-group>
            <!-- 本月的记录 -->
            <el-menu-item-group>
              <template #title><span>本月</span></template>
              <el-menu-item v-for="(chat, index) in chatDataThisMonth" :key="'thismonth-' + index">
                {{ chat.prompt }}
              </el-menu-item>
            </el-menu-item-group>
            <!-- 更久之前的记录 -->
            <el-menu-item-group>
              <template #title><span>更久之前</span></template>
              <el-menu-item v-for="(chat, index) in chatDataOlder" :key="'older-' + index">
                {{ chat.prompt }}
              </el-menu-item>
            </el-menu-item-group>
          </el-sub-menu>
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
          <!-- 对话主体 -->
          <div v-for="(message, index) in chatHistory" :key="index" class="chat-message">
            <div v-if="message.type === 'user'">
              <strong>User:</strong> {{ message.content }}
            </div>
            <div v-else>
              <strong>Bot:</strong>
              <img v-if="message.content.picture" :src="message.content.picture" alt="Response Image" />
              <p v-else>No image generated.</p>
            </div>
          </div>
        </el-main>
        <!-- 输入框 -->
        <el-input
          v-model="input"
          :autosize="{ minRows: 1, maxRows: 5 }"
          type="textarea"
          placeholder="Please input"
          clearable
          @keyup.enter.native="handleSubmit"
        />
      </el-main>
    </el-container>
  </div>
  <router-view></router-view>
</template>

<style scoped>

</style>