<script lang="ts">
import { ref } from 'vue';
export default {
  data() {
    return {
      isLogin: ref(true),
      loginForm: ref({
        username: '',
        password: ''
      }),
      registerForm: ref({
        username: '',
        password: '',
        confirmPassword: ''
      }),
      loginRules: {
        username: [
          { required: true, message: '请输入用户名', trigger: 'blur' }
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' }
        ]
      },
      registerRules: {
        username: [
          { required: true, message: '请输入用户名', trigger: 'blur' }
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' }
        ],
        confirmPassword: [
          { required: true, message: '请确认密码', trigger: 'blur' },
        ]
      }
    };
  },
  methods: {
    // 登录表单提交
    submitLoginForm(this: any, formName: string) {
      this.$refs[formName].validate((valid: any) => {
        if (valid) {
          this.$message.success('登录成功！');
          // 登录逻辑，如API调用
        } else {
          this.$message.error('请正确填写表单');
        }
      });
    },
    // 注册表单提交
    submitRegisterForm(this: any, formName: string) {
      this.$refs[formName].validate((valid: any) => {
        if (valid) {
          this.$message.success('注册成功！');
          // 注册逻辑，如API调用
        } else {
          this.$message.error('请正确填写表单');
        }
      });
    },
    // 重置表单
    resetForm(this: any, formName: string) {
      this.$refs[formName].resetFields();
    },
    // 切换到注册
    switchToRegister() {
      this.isLogin = false;
    },
    // 切换到登录
    switchToLogin() {
      this.isLogin = true;
    }
  }
};
</script>

<template>
  <div class="auth-container">
    <el-card class="auth-card">
      <div v-if="isLogin">
        <h2>登录</h2>
        <el-form :model="loginForm" :rules="loginRules" ref="loginForm" label-width="80px">
          <el-form-item label="用户名" prop="username">
            <el-input v-model="loginForm.username" placeholder="请输入用户名"></el-input>
          </el-form-item>
          <el-form-item label="密码" prop="password">
            <el-input v-model="loginForm.password" placeholder="请输入密码" show-password></el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="submitLoginForm('loginForm')">登录</el-button>
            <el-button @click="resetForm('loginForm')">重置</el-button>
          </el-form-item>
        </el-form>
        <p>还没有账户？<el-button @click="switchToRegister">注册</el-button></p>
      </div>

      <div v-else>
        <h2>注册</h2>
        <el-form :model="registerForm" :rules="registerRules" ref="registerForm" label-width="80px">
          <el-form-item label="用户名" prop="username">
            <el-input v-model="registerForm.username" placeholder="请输入用户名"></el-input>
          </el-form-item>
          <el-form-item label="密码" prop="password">
            <el-input v-model="registerForm.password" placeholder="请输入密码" show-password></el-input>
          </el-form-item>
          <el-form-item label="确认密码" prop="confirmPassword">
            <el-input v-model="registerForm.confirmPassword" placeholder="请确认密码" show-password></el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="submitRegisterForm('registerForm')">注册</el-button>
            <el-button @click="resetForm('registerForm')">重置</el-button>
          </el-form-item>
        </el-form>
        <p>已有账户？<el-button @click="switchToLogin">登录</el-button></p>
      </div>
    </el-card>
  </div>
</template>

<style scoped>
.auth-container {
  height: 40%;
  width: 40%;
  position: absolute;
  top: 30%;
  left: 30%;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #f5f5f5;
}

.auth-card {
  height: 100%;
  width: 100%;
  padding: 20px;
  text-align: center;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.auth-card h2 {
  margin-bottom: 20px;
  font-size: 24px;
}
</style>