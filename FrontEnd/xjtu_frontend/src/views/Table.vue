<template>
    <div class="table-page">
      <div class="table-header">
        <h2>数据列表</h2>
      </div>
  
      <el-table :data="tableData" border style="width: 100%" v-loading="loading">
        <el-table-column prop="account" label="用户名" width="180" />
        <el-table-column prop="pwd" label="密码" width="180" />
        <el-table-column prop="email" label="邮箱" />
      </el-table>
      
      <div class="pagination">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 30, 50]"
          :total="total"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          layout="total, sizes, prev, pager, next"
        />
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import axios from 'axios'  // 需要先运行: npm install axios
  
  const loading = ref(false)
  const currentPage = ref(1)
  const pageSize = ref(10)
  const total = ref(0)
  const tableData = ref([])
  
  // 获取表格数据的函数
  const getTableData = async () => {
    loading.value = true
    try {
      const response = await axios.get('http://localhost:8080/listUser')  // 添加 await
      const allData = response.data
      console.log(allData)
      total.value = allData.length
      
      const startIndex = (currentPage.value - 1) * pageSize.value
      const endIndex = startIndex + pageSize.value
      tableData.value = allData.slice(startIndex, endIndex)
    } catch (error) {
      console.error('获取数据失败:', error)
    } finally {
      loading.value = false
    }
  }
  
  // 每页条数改变时的处理函数
  const handleSizeChange = (val) => {
    pageSize.value = val
    getTableData()
  }
  
  // 页码改变时的处理函数
  const handleCurrentChange = (val) => {
    currentPage.value = val
    getTableData()
  }
  
  // 页面加载时获取数据
  onMounted(() => {
    getTableData()
  })
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