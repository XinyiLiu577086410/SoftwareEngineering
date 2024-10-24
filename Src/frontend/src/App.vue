<script lang="ts">
import { RouterLink, RouterView } from 'vue-router'
import { ref } from 'vue';
export default {
  data () {
    return {
      alreadyLoggedin : ref(false),
      isCollapse : ref(false),
      circleUrl : ref('https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png'),
      input : ref(''),
    }
  },
  methods () {
    return {
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
          <router-link to="/user">
            <!-- 头像 -->
            <el-avatar :size="50" :src="circleUrl"/>
          </router-link>
          <router-link to="/login">
            <!-- 登录 -->
            <el-button>登录</el-button>
          </router-link>
          <!-- 登出按钮 -->
          <el-button>登出</el-button>
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