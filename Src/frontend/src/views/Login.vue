<script lang="ts">
import { ref } from 'vue';
import { useloginStatus } from '@/stores/loginStatus';

export default {
  data() {
    return {
      loginStatus : null,
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
    async submitLoginForm(this: any, formName: string) {
      this.$refs[formName].validate(async (valid: boolean) => {
        if (valid) {
          try {
            const response = await this.$axios.post('/api/login', this.loginForm);
            if (response.data.result === 0) {
              this.$message.success('登录成功');
              this.loginStatus.setLoginStatus(true);
              this.loginStatus.setUsername(this.loginForm.username);
              this.$router.push('/');
            } else if (response.data.result === -2) {
              this.$message.error('用户不存在');
            } else if (response.data.result === -3) {
              this.$message.error('密码错误');
            } else {
              this.$message.error('登录失败');
            }
          } catch (error) {
            console.error(error);
            this.$message.error('登录请求出错，请稍后重试');
          }
        } else {
          this.$message.error('请正确填写表单');
        }
      });
    },
    // 注册表单提交
    async submitRegisterForm(this: any, formName: string) {
      this.$refs[formName].validate(async (valid: any) => {
        if (valid) {
          try {
            console.log(this.registerForm)
            const response = await this.$axios.post('/api/register', this.registerForm);
            console.log(response.data)
            if (response.data.result == 0) {
              this.$message.success('注册成功');
              this.switchToLogin();
              this.$router.push('/login');
            } else {
              this.$message.error('注册失败');
            }
          } catch (error) {
            // 处理请求错误
            console.error(error);
            this.$message.error('注册请求失败，请稍后重试');
          }
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
  },
  created() {
    this.loginStatus = useloginStatus();
  },
};
</script>

<template>
  <div class="auth-container">
    <el-card class="auth-card">
      <router-link to="/">
        <el-button>首页</el-button>
      </router-link>
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