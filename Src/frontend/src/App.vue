<script setup lang="ts">
// import { RouterLink, RouterView } from 'vue-router'
import { ref } from 'vue'
const isCollapse = ref(false)
const circleUrl = 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png'
const input = ref('')
</script>

<template>
  <div class="full">
    <el-container>
      <el-aside>
        <!-- 目录栏 -->
        <el-menu default-active="2" class="el-menu-vertical" :collapse="isCollapse">
          <el-sub-menu index="1">
            <template #title>
              <el-icon><location /></el-icon>
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
            <el-icon><icon-menu /></el-icon>
            <template #title>Navigator Two</template>
          </el-menu-item>
        </el-menu>
        <el-aside style="height: 40%;">
        </el-aside>
        <!-- 头像 -->
        <el-avatar :size="50" :src="circleUrl" />
        <!-- 登出按钮 -->
        <el-button>登出</el-button>
      </el-aside>
      <el-main>
          <el-main style="height: 80%;">
          </el-main>
          <!-- 输入框 -->
          <el-input
          v-model="input"
          :autosize="{ minRows: 1, maxRows: 5 }"
          type="textarea"
          placeholder="Please input"
          clearable
        />
      </el-main>
    </el-container>
  </div>
</template>

<style scoped>

.full {
  height: 100%;
  width: 100%;
  position: absolute;
  top: 0;
  left: 0;
}
.el-container {
  height: 100%;
  width: 100%;
  /* display: flex; */
  /* flex-direction: column;
  justify-content: space-between; */
}

.el-header,
.el-footer {
  background-color: #b3c0d1;
  color: #333;
}

.el-aside {
  background-color: #d3dce6;
  color: #333;
}

.el-main {
  background-color: #fbf6f6;
  color: #333;
}

.el-menu {
  background-color: #d3dce6;
}

.el-menu-vertical:not(.el-menu--collapse) {
  /* width: 200px; */
  min-height: 400px;
}

</style>