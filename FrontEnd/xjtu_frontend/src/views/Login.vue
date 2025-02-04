<template>
  <div class="login-container">
    <div class="login-box">
      <h2>用户登录</h2>
      
      <div class="form-group" v-if="!showForgotPassword">
        <input
          type="text"
          v-model="username"
          placeholder="请输入用户名"
          class="form-input"
        >
      </div>
      
      <div class="form-group" v-if="!showForgotPassword">
        <input
          type="password"
          v-model="password"
          placeholder="请输入密码"
          class="form-input"
        >
      </div>
      
      <div v-if="errorMessage" class="error-message">
        {{ errorMessage }}
      </div>
      
      <button @click="handleLogin" class="login-button" v-if="!showForgotPassword">
        登录
      </button>
      
      <div class="additional-links">
        <a href="#" @click.prevent="toggleForgotPassword">忘记密码？</a>
        <a href="#">注册账号</a>
      </div>
      
      <!-- 忘记密码表单 -->
      <div v-if="showForgotPassword" class="forgot-password-form">
        <h3>忘记密码</h3>
        <div class="form-group">
          <input
            type="email"
            v-model="email"
            placeholder="请输入注册邮箱"
            class="form-input"
          >
        </div>
        <button @click="handleForgotPassword" class="login-button">
          提交
        </button>
        <div class="additional-links">
          <a href="#" @click.prevent="toggleForgotPassword">返回登录</a>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'  // 确保已经安装并导入 axios
import { useRouter } from 'vue-router'  // 导入路由

const router = useRouter()
const username = ref('')
const password = ref('')
const email = ref('')
const errorMessage = ref('')
const showForgotPassword = ref(false)

const handleLogin = async () => {
  // 表单验证
  if (!username.value || !password.value) {
    errorMessage.value = '用户名和密码不能为空'
    return
  }

  try {
    console.log('发送登录请求:', {
      account: username.value,
      pwd: password.value
    })

    const response = await axios.post('http://localhost:8080/user/login', 
      {
        account: username.value,
        pwd: password.value
      },
      {
        headers: {
          'Content-Type': 'application/json',
        },
        withCredentials: true  // 允许携带凭证
      }
    )

    console.log('登录响应:', response.data)

    if (response.data.code === 200) {  // 假设后端返回 code 200 表示成功
      // 登录成功，可以存储token或用户信息
      localStorage.setItem('token', response.data.token)  // 如果后端返回token
      localStorage.setItem('user', JSON.stringify(response.data.user))  // 存储用户信息
      
      // 跳转到首页或其他页面
      router.push('/table')  // 确保你有一个名为 home 的路由
    } else {
      errorMessage.value = response.data.msg || '登录失败'
      alert(errorMessage.value);
    }
  } catch (error) {
    console.error('登录错误详情:', error.response || error)
    errorMessage.value = error.response?.data?.message || '登录失败，请稍后重试'
  }
}

const handleForgotPassword = async () => {
  // 表单验证
  if (!email.value) {
    errorMessage.value = '邮箱不能为空'
    return
  }

  try {
    console.log('发送忘记密码请求:', {
      email: email.value
    })

    const response = await axios.post('http://localhost:8080/user/forgot-password', 
      {
        email: email.value
      },
      {
        headers: {
          'Content-Type': 'application/json',
        },
        withCredentials: true  // 允许携带凭证
      }
    )

    console.log('忘记密码响应:', response.data)

    if (response.data.code === 200) {  // 假设后端返回 code 200 表示成功
      alert('重置密码邮件已发送，请查收')
      toggleForgotPassword()
    } else {
      errorMessage.value = response.data.msg || '操作失败'
      alert(errorMessage.value);
    }
  } catch (error) {
    console.error('忘记密码错误详情:', error.response || error)
    errorMessage.value = error.response?.data?.message || '操作失败，请稍后重试'
  }
}

const toggleForgotPassword = () => {
  showForgotPassword.value = !showForgotPassword.value
  errorMessage.value = ''
}
</script>

<style scoped>
/* 添加这些全局样式确保页面占满整个视口 */
:root {
  height: 100%;
}

body {
  height: 100%;
  margin: 0;
}

.login-container {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #f5f5f5;
  /* 可以添加背景图片 */
  background-image: url('@/assets/background.jpg');
  background-size: cover;
  background-position: center;
}

.login-box {
  width: 100%;
  max-width: 400px;
  padding: 40px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  margin: 20px;  /* 添加边距防止在小屏幕上贴边 */
}

h2 {
  text-align: center;
  color: #333;
  margin-bottom: 30px;
}

.form-group {
  margin-bottom: 20px;
}

.form-input {
  width: 100%;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  transition: border-color 0.3s;
}

.form-input:focus {
  border-color: #409eff;
  outline: none;
}

.login-button {
  width: 100%;
  padding: 12px;
  background-color: #409eff;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.login-button:hover {
  background-color: #66b1ff;
}

.error-message {
  color: #f56c6c;
  font-size: 14px;
  margin-bottom: 20px;
  text-align: center;
}

.additional-links {
  margin-top: 20px;
  text-align: center;
}

.additional-links a {
  color: #409eff;
  text-decoration: none;
  margin: 0 10px;
  font-size: 14px;
}

.additional-links a:hover {
  text-decoration: underline;
}

.forgot-password-form {
  margin-top: 20px;
}
</style>