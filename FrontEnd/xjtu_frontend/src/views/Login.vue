<template>
  <div class="login-container">
    <div class="login-box">
      <h2 v-if="!showForgotPassword && !showRegister">用户登录</h2>
      <h2 v-if="showRegister">注册账号</h2>
      
      <div class="form-group" v-if="!showForgotPassword && !showRegister">
        <input
          type="text"
          v-model="username"
          placeholder="请输入用户名"
          class="form-input"
        >
      </div>
      
      <div class="form-group" v-if="!showForgotPassword && !showRegister">
        <input
          type="password"
          v-model="password"
          placeholder="请输入密码"
          class="form-input"
        >
      </div>
      
      <div class="form-group" v-if="showRegister">
        <input
          type="text"
          v-model="newUsername"
          placeholder="请输入新用户名"
          class="form-input"
        >
      </div>
      
      <div class="form-group" v-if="showRegister">
        <input
          type="password"
          v-model="newPassword"
          placeholder="请输入新密码"
          class="form-input"
        >
      </div>
      
      <div class="form-group" v-if="showRegister">
        <input
          type="email"
          v-model="email"
          placeholder="请输入注册邮箱"
          class="form-input"
        >
      </div>

      <div class="form-group" v-if="showRegister">
        <div class="inline-form">
          <input
            type="text"
            v-model="verifyCode"
            placeholder="请输入验证码"
            class="form-input inline-input"
          > 
          <el-button 
            type="primary" 
            @click="handleSendVerifyCode" 
            :disabled="countdown > 0"
          >
            {{ countdown > 0 ? `${countdown}秒后重试` : '发送验证码' }}
          </el-button>
        </div>
      </div>
      
      <div v-if="errorMessage" class="error-message">
        {{ errorMessage }}
      </div>
      
      <button @click="handleLogin" class="login-button" v-if="!showForgotPassword && !showRegister">
        登录
      </button>
      
      <button @click="handleRegister" class="login-button" v-if="showRegister">
        注册
      </button>
      
      <div class="additional-links">
        <a href="#" @click.prevent="toggleForgotPassword" v-if="!showForgotPassword && !showRegister">忘记密码？</a>
        <a href="#" @click.prevent="toggleRegister" v-if="!showForgotPassword && !showRegister">注册账号</a>
        <a href="#" @click.prevent="toggleRegister" v-if="showRegister">返回登录</a>
      </div>
      
      <!-- 忘记密码表单 -->
      <div v-if="showForgotPassword" class="forgot-password-form">
        <h2>忘记密码</h2>
        <div class="form-group">
          <input
            type="email"
            v-model="email"
            placeholder="请输入注册邮箱"
            class="form-input"
          >
        </div>
        <div class="form-group">
          <input
            type="text"
            v-model="FirstPassword"
            placeholder="请输入新密码"
            class="form-input"
          ></input>
        </div>
        <div class="form-group">
          <input
            type="text"
            v-model="SecondPassword"
            placeholder="再次输入密码"
            class="form-input"
          ></input> 
        </div>
        <div class="form-group">
          <div class="inline-form">
          <input
            type="text"
            v-model="verifyCode"
            placeholder="请输入验证码"
            class="form-input inline-input"
          > 
          <el-button 
            type="primary" 
            @click="handleSendVerifyCode" 
            :disabled="countdown > 0"
          >
            {{ countdown > 0 ? `${countdown}秒后重试` : '发送验证码' }}
          </el-button>
        </div>
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
const newUsername = ref('')
const newPassword = ref('')
const FirstPassword = ref('')
const SecondPassword = ref('')
const email = ref('')
const errorMessage = ref('')
const showForgotPassword = ref(false)
const showRegister = ref(false)
const countdown = ref(0)  // 新增倒计时变量
const verifyCode = ref('')

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
      router.push('/neo4j')  // 确保你有一个名为 home 的路由
    } else {
      errorMessage.value = response.data.msg || '登录失败'
      alert(errorMessage.value);
    }
  } catch (error) {
    console.error('登录错误详情:', error.response || error)
    errorMessage.value = error.response?.data?.message || '登录失败，请稍后重试'
  }
}

const handleRegister = async () => {
  // 表单验证
  if (!newUsername.value || !newPassword.value || !email.value || !isValidEmail(email.value) || !verifyCode.value) {
    errorMessage.value = '用户名、密码和邮箱验证码不能为空'
    return
  }

  try {
    console.log('发送注册请求:', {
      username: newUsername.value,
      password: newPassword.value,
      email: email.value,
      verifyCode: verifyCode.value
    })

    const response = await axios.post('http://localhost:8080/user/register', 
      {
        username: newUsername.value,
        password: newPassword.value,
        email: email.value,
        verifyCode: verifyCode.value
      },
      {
        headers: {
          'Content-Type': 'application/json',
        },
        withCredentials: true  // 允许携带凭证
      }
    )

    console.log('注册响应:', response.status)

    if (response.status === 202) {  // 假设后端返回 code 202 表示成功
      showRegister.value = false
      showForgotPassword.value = false
      alert('注册成功，请登录')
    } else {
      errorMessage.value = response.data.msg || '注册失败'
      alert(errorMessage.value);
    }
  } catch (error) {
    console.error('注册错误详情:', error.response || error)
    errorMessage.value = error.response?.data?.message || '注册失败，请稍后重试'
  }
}

const handleForgotPassword = async () => {
  // 表单验证
  if (!email.value || !isValidEmail(email.value)) {
    errorMessage.value = '邮箱不能为空'
    return
  }
  if(FirstPassword.value !== SecondPassword.value){
    alert("两次密码不一致")
    return
  }
  if(FirstPassword.value == null || SecondPassword.value == null || FirstPassword.value == '' || SecondPassword.value == ''){
    alert("密码不能为空")
    return
  }
  try{
    console.log('发送忘记密码请求:', {
      email: email.value,
      password: FirstPassword.value,
      verifyCode: verifyCode.value
    })
    const response = await axios.post('http://localhost:8080/user/forgetPassword', 
      {
        email: email.value,
        password: FirstPassword.value,
        verifyCode: verifyCode.value
      },
      {
        headers: {
          'Content-Type': 'application/json',
        },
        withCredentials: true  // 允许携带凭证
      },
    )
    console.log(response)
    if(response.status === 202){
        alert("修改成功")
        showForgotPassword.value = false
        showRegister.value = false
      }else if(response.status === 400){
        alert("修改失败,邮箱未注册")
      }else if(response.status === 208){
        alert("验证码已过期")
      }else{
        alert("验证码已发送，请勿重复点击")
      }
  }catch(error){
    alert("操作错误")
  }
}

const toggleForgotPassword = () => {
  showForgotPassword.value = !showForgotPassword.value
  errorMessage.value = ''
}

const toggleRegister = () => {
  showRegister.value = !showRegister.value
  errorMessage.value = ''
}
const isValidEmail = (email) => {
  const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
  return emailRegex.test(email);
}

const handleSendVerifyCode = async() => {
  if (!isValidEmail(email.value)) {
    alert("请输入有效的邮箱地址")
    return
  }
  try {
    console.log('发送忘记密码请求:', {
      email: email.value
    })

    const response = await axios.post('http://localhost:8080/sendEmail', 
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

    console.log('忘记密码响应:', response)

    if (response.status === 202) {  // 假设后端返回 code 200 表示成功
      alert('邮件已发送，请查收')

    }else if(response.status === 208){
      alert("验证码已发送，请误重复点击")
    } 
    else {
      errorMessage.value = response.data.msg || '操作失败'
      alert(errorMessage.value);
    }
  } catch (error) {
    console.error('忘记密码错误详情:', error.response || error)
    errorMessage.value = error.response?.data?.message || '操作失败，请稍后重试'
  }

  console.log('发送验证码逻辑')
  startCountdown()  // 发送验证码后开始倒计时
}

const startCountdown = () => {
  countdown.value = 60
  const timer = setInterval(() => {
    if (countdown.value > 0) {
      countdown.value--
    } else {
      clearInterval(timer)
    }
  }, 1000)
}
</script>

<style scoped>
/* 添加这些全局样式确保页r占满整个视口 */
root {
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
  background-image: url('https://img.freepik.com/free-vector/japanese-wave-line-art-landscape-background-abstract-mountain-banner-design-pattern-vector-illustration-geometric-poster_90220-714.jpg?t=st=1745911016~exp=1745914616~hmac=b5c83e8390bf9df648dde0c496f8fec25e38ac1b88a8ccb796675d294addd44b&w=1800');
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

.inline-form {
  display: flex;
  align-items: center;
}

.inline-input {
  flex: 1;
  margin-right: 10px;
}

.el-button {
  height: 42px;
}
</style>