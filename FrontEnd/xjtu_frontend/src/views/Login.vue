<template>
    <div class="login-container">
      <div class="login-box">
        <h2>用户登录</h2>
        
        <div class="form-group">
          <input
            type="text"
            v-model="username"
            placeholder="请输入用户名"
            class="form-input"
          >
        </div>
        
        <div class="form-group">
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
        
        <button @click="handleLogin" class="login-button">
          登录
        </button>
        
        <div class="additional-links">
          <a href="#">忘记密码？</a>
          <a href="#">注册账号</a>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  
  const username = ref('')
  const password = ref('')
  const errorMessage = ref('')
  
  const handleLogin = () => {
    if (!username.value || !password.value) {
      errorMessage.value = '用户名和密码不能为空'
      return
    }
    console.log('登录信息：', {
      username: username.value,
      password: password.value
    })
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
  </style>