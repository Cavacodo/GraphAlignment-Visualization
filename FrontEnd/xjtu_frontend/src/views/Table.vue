<template>
  <div style="display: flex; flex-direction: column; align-items: center;">
    <el-table :data="tableData" style="width: 100%; max-width: 400px; margin-bottom: 10px;">
      <el-table-column prop="singleColumn" label="结果"></el-table-column>
    </el-table>
    <div>
      <el-button type="primary" @click="handleMethod1" :disabled="isButtonDisabled">方法1</el-button>
      <el-button type="primary" @click="handleMethod2">方法2</el-button>
    </div>
  </div>
</template>

<script setup>
  import { ref, onMounted, onBeforeUnmount } from 'vue'
  import axios from 'axios'  // 需要先运行: npm install axios

  const res = ref(null)
  const loading = ref(false)
  const currentPage = ref(1)
  const pageSize = ref(10)
  const total = ref(0)
  const tableData = ref([])
  const isButtonDisabled = ref(true)  // 新增按钮禁用状态变量

  // 获取表格数据的函数
  const getTableData = async () => {
    loading.value = true
    try {
      const response = await axios.post('http://localhost:8080/res/getRes')  // 添加 await
      let allData = response.data
      console.log(allData)
      
      // 检查 allData 是否为数组，如果不是则转换为数组
      if (!Array.isArray(allData)) {
        allData = [allData]
      }
      
      // 将 allData 转换为包含 singleColumn 属性的对象数组
      allData = allData.map(item => ({ singleColumn: item }))
      
      total.value = allData.length
      
      const startIndex = (currentPage.value - 1) * pageSize.value
      const endIndex = startIndex + pageSize.value
      tableData.value = allData.slice(startIndex, endIndex)

      // 如果数据不为空，停止轮询并启用按钮
      if (allData.length > 0) {
        clearInterval(pollInterval)
        isButtonDisabled.value = false  // 启用按钮
      }
    } catch (error) {
      console.error('获取数据失败:', error)
    } finally {
      loading.value = false
    }
  }

  // 使用 setInterval 实现轮询访问
  let pollInterval = null

  const setupPolling = () => {
    // TODO 在点击按钮之后才发送请求，而不是在页面加载时立即发送请求
    pollInterval = setInterval(getTableData, 500)  // 每5秒轮询一次
  }

  // 页面加载时设置轮询
  onMounted(() => {
    isButtonDisabled.value = false
    // setupPolling()
  })

  // 页面卸载时清除轮询
  onBeforeUnmount(() => {
    clearInterval(pollInterval)
  })

  // 方法1的处理函数
  const handleMethod1 = async() => {
    console.log('方法1被点击')
    isButtonDisabled.value = true  // 禁用按钮
    let timer = null

    try {
      // 设置6秒计时器
      timer = setTimeout(() => {
        alert('请求超时')
        isButtonDisabled.value = false  // 恢复按钮
      }, 6000)
      const response = await axios.post('http://localhost:8080/api/send',
      {
        type: 1
      },
      {
        headers: {
          'Content-Type': 'application/json',
        },
        withCredentials: true  // 允许携带凭证
      }
      )
      if (response.status === 200) {
        // 检查 response.data 是否为数组，如果不是则转换为数组
        let allData = response.data
        if (!Array.isArray(allData)) {
          allData = [allData]
        }

        // 将 allData 转换为包含 singleColumn 属性的对象数组
        allData = allData.map(item => ({ singleColumn: item }))

        // 将 response.data 赋值给 tableData
        tableData.value = allData
        isButtonDisabled.value = false
        clearTimeout(timer)  // 清除计时器
      } else {
        console.log(error)
      }
    } catch (error) {
      console.log(error)  
    }
  }

  // 方法2的处理函数
  const handleMethod2 = async() => {
    console.log('方法2被点击')
    isButtonDisabled.value = true  // 禁用按钮
    let timer = null

    try {
      // 设置6秒计时器
      timer = setTimeout(() => {
        alert('请求超时')
        isButtonDisabled.value = false  // 恢复按钮
      }, 6000)
      const response = await axios.post('http://localhost:8080/api/send',
      {
        type: 2
      },
      {
        headers: {
          'Content-Type': 'application/json',
        },
        withCredentials: true  // 允许携带凭证
      }
      )
      if (response.status === 200) {
        console.log(response.data)
        // 检查 response.data 是否为数组，如果不是则转换为数组
        let allData = response.data
        if (!Array.isArray(allData)) {
          allData = [allData]
        }

        // 将 allData 转换为包含 singleColumn 属性的对象数组
        allData = allData.map(item => ({ singleColumn: item }))

        // 将 response.data 赋值给 tableData
        tableData.value = allData
        isButtonDisabled.value = false
        clearTimeout(timer)  // 清除计时器
      } else {
        console.log(error)
      }
    } catch (error) {
      console.log(error)  
    }
  }
</script>

<style scoped>
  .table-page {
    padding: 20px;
  }
  
  .table-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
  }
  
  .pagination {
    margin-top: 20px;
    display: flex;
    justify-content: flex-end;
  }
</style>