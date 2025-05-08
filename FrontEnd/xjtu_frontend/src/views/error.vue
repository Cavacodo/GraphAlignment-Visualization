<template>
    <div class="error-container">
      <div class="error-content">
        <h1 class="font">错误</h1>
        <p>{{ message }}</p>
        <el-button type="primary" @click="goToLogin">返回登录</el-button>
      </div>
    </div>
  </template>
  
  <script setup>
  import { useRouter, useRoute } from 'vue-router'
  
  const router = useRouter()
  const route = useRoute()
  
  const message = route.query.message || '发生未知错误'
  
  const goToLogin = () => {
    router.push({ name: 'Login' })
  }
  </script>
  
  <style scoped>
  .error-container {
    height: 100vh;
    width: 100vw;
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: #f5f5f5;
  }
  
  .error-content {
    text-align: center;
    align-items: center;
    display: flex;
    flex-direction: column;
    justify-content: center;
    background: white;
    width: 90%;
    height: 80%;
    padding: 40px;
    border-radius: 12px;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.2);
  }
  
  .error-content h1 {
    font-size: 45px;
    margin-bottom: 16px;
    color: #ff4d4f;
  }
  
  .error-content p {
    font-size: 24px;
    margin-bottom: 24px;
  }

  
  .error-content .el-button {
    margin-top: 20px;
  }
 
  </style>