<template>
  <div class="main-container">
    <div class="display-layout">
      <el-aside width="200px">
        <Sidebar />
      </el-aside>

      <div class="card-container">
        <el-card class="card">
          <div class="form-container">
            <span class="section-title">用户信息</span>
            <!-- 用户信息 -->
            <el-form :model="userInfo" label-position="left" class="info-form">
              <el-form-item label="用户名称">
                <el-input v-model="userInfo.username" disabled />
              </el-form-item>

              <el-form-item label="绑定邮箱">
                <el-input v-model="userInfo.email" disabled/>
              </el-form-item>

              <el-form-item label="用户权限">
                <el-input v-model="userInfo.role" disabled />
              </el-form-item>
            </el-form>
            <!-- 修改后的 span 样式 -->
            <span class="section-title">修改密码</span>
            <!-- 密码修改 -->
            <el-form :model="passwordForm" :rules="passwordRules" ref="passwordFormRef" label-position="left" class="password-form">
              <el-form-item label="输入旧密码" prop="oldPassword">
                <el-input v-model="passwordForm.oldPassword" type="password" />
              </el-form-item>

              <el-form-item label="输入新密码" prop="newPassword">
                <el-input v-model="passwordForm.newPassword" type="password" />
              </el-form-item>

              <el-form-item label="确认新密码" prop="confirmPassword">
                <el-input v-model="passwordForm.confirmPassword" type="password" />
              </el-form-item>

              <el-form-item>
                <el-button type="primary" @click="submitPasswordChange">确定</el-button>
                <!-- 新增间距 -->
                <span style="width: 200px; display: inline-block;"></span>
                <!-- 新增登出按钮 -->
                <el-button type="warning" @click="logout">登出</el-button>
              </el-form-item>
            </el-form>
          </div>
        </el-card>
      </div>
    </div>
  </div>
</template>

<script>
import Sidebar from '../components/SideBar.vue'
import axios from 'axios'
import { ElMessage } from 'element-plus'
import { useRouter, useRoute } from 'vue-router'


export default {
  components: { Sidebar },
  data() {
    return {
      userInfo: {
        username: localStorage.getItem('user'),
        email: '',
        role: localStorage.getItem('role'),
      },
      passwordForm: {
        oldPassword: '',
        newPassword: '',
        confirmPassword: '',
      },
      passwordRules: {
        oldPassword: [{ required: true, message: '请输入旧密码', trigger: 'blur' }],
        newPassword: [{ required: true, message: '请输入新密码', trigger: 'blur' }],
        confirmPassword: [
          { required: true, message: '请确认新密码', trigger: 'blur' },
          {
            validator: (rule, value, callback) => {
              if (value !== this.passwordForm.newPassword) {
                callback(new Error('两次输入的密码不一致'))
              } else {
                callback()
              }
            },
            trigger: 'blur',
          },
        ],
      },
      router : useRouter()
    }
  },
  mounted() {
    this.fetchUserInfo()
  },
  methods: {
    fetchUserInfo() {
      axios.get('http://localhost:8080/user/getEmailByName', {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`
        },
        params: {
          name: localStorage.getItem('user')
        }
      }).then(res => {
        this.userInfo.email = res.data
      }).catch(() => {
        ElMessage.error('获取用户信息失败')
      })
    },
    submitPasswordChange() {
      this.$refs.passwordFormRef.validate(valid => {
        if (valid) {
          console.log(localStorage.getItem('user'))
          console.log(this.passwordForm.oldPassword)
          console.log(this.passwordForm.newPassword)
          axios.post('http://localhost:8080/user/changeUserPwd', {
            account: localStorage.getItem('user'),
            oldpwd: this.passwordForm.oldPassword,
            newpwd: this.passwordForm.newPassword
          }, {
            headers: {
              Authorization: `Bearer ${localStorage.getItem('token')}`
            }
          }).then(() => {
            ElMessage.success('密码修改成功')
            this.passwordForm.oldPassword = ''
            this.passwordForm.newPassword = ''
            this.passwordForm.confirmPassword = ''
            this.router.push({ path: '/login' })
          }).catch(() => {
            ElMessage.error('密码修改失败')
          })
        }
      })
    },
    // 新增登出方法
    logout() {
      localStorage.clear();
      this.router.push({ name: 'Login' })
    }
  }
}
</script>

<style scoped>
.main-container {
  height: 100vh;
  width: 100vw;
  background-color: #dedee0;
  margin: 0;
  padding: 0;
}

.display-layout {
  display: flex;
  height: 100%;
  width: 100%;
}

.el-card {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.card-container {
  padding: 10px;
  height: 100%;
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.form-container {
  width: 400px;
  display: flex;
  flex-direction: column;
  gap: 15px; /* 调整间距，使内容更紧凑 */
}

.el-form-item {
  width: 100%;
  text-align: left; /* 确保表单项内容左对齐 */
}

/* 新增样式：调整 span 字体大小并左对齐 */
.section-title {
  font-size: 24px;
  display: inline-block;
  text-align: left;
  margin-bottom: 10px; /* 添加底部间距 */
}
</style>