<template>
  <div class="main-container">
    <div class="display-layout">
      <!-- 左侧边栏 -->
      <el-aside width="200px">
        <Sidebar />
      </el-aside>
      <div class="card-container">
        <el-card class="card">
          <div class="header-select">
            <span class="blank"></span>
            <el-cascader v-model="value" :options="options" @change="handleChange" />
            <el-button @click="searchSubmit">搜索</el-button>
          </div>
          <el-table :data="tableData" style="width: 100%">
            <!-- 动态列渲染 -->
            <el-table-column v-for="col in tableColumns" :key="col.prop" :prop="col.prop" :label="col.label" />

            <!-- 固定操作列 -->
            <el-table-column label="Operations" fixed="right" width="150">
              <template #default="scope">
                <el-button link type="danger" size="small" @Click="handleDelete(scope.row.id)"
                  :disabled="scope.row.account === 'admin'">Delete</el-button>
              </template>
            </el-table-column>
          </el-table>
          <el-pagination background layout="prev, pager, next" :total="total" :page-size="pageSize"
            :current-page="currentPage" @current-change="handlePageChange" />
          <el-dialog v-model="deletedialogVisible" title="Delete Row" width="400px">
            <div style="text-align: left;">
              <span style="font-size: 18px;">确定删除吗？此操作不可逆</span>
            </div>
            <template #footer>
              <el-button @click="deletedialogVisible = false">Cancel</el-button>
              <el-button type="primary" @click="submitDelete">Save</el-button>
            </template>
          </el-dialog>
        </el-card>
      </div>

    </div>
  </div>
</template>

<script>
import Sidebar from '../components/SideBar.vue';
import { Card } from 'ant-design-vue';
import { useRouter, useRoute } from 'vue-router'
import axios from 'axios';

export default {
  components: { Card, Sidebar },
  data() {
    return {
      username: '',
      searchedData: [],
      colName: '',
      searchName: '',
      fullData: [],
      originalData: [],
      tableData: [],       // 后端数据
      tableColumns: [],
      editForm: [],
      deletingId: '',
      value: ['user'],
      currentPage: 1,      // 当前页码
      pageSize: 7,        // 每页条数
      total: 0,
      dialogVisible: false,
      editDisabledMap: {},
      input: '',
      deletedialogVisible: false,
      options: [{
        value: 'IsoRank',
        label: 'IsoRank',
      }, {
        value: 'REGAL',
        label: 'REGAL',
      }, {
        value: 'DeepLink',
        label: 'DeepLink',
      }, {
        value: 'BigAlign',
        label: 'BigAlign',
      }, {
        value: 'FINAL',
        label: 'FINAL',
      }, {
        value: 'GAlign',
        label: 'GAlign',
      }, {
        value: 'GTCAlign',
        label: 'GTCAlign'
      }

      ]    // 根据数据自动生成
    };
  },
  methods: {
    fetchData() {
      this.username = localStorage.getItem('user');
      axios.get('http://localhost:8080/exp/getExpByAccount', {
        params: {
          account: this.username
        },
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`
        }
      }).then(res => {
        this.fullData = res.data;
        this.originalData = [...res.data];
        this.total = this.fullData.length;  // ✅ 设置总条数
        this.updateTableData();
        this.tableColumns = Object.keys(res.data[0]).map(key => ({
          prop: key,
          label: key
        }));
      });
    },

    updateTableData() {
      const start = (this.currentPage - 1) * this.pageSize;
      const end = start + this.pageSize;
      this.tableData = this.fullData.slice(start, end);
    },
    handlePageChange(newPage) {
      this.currentPage = newPage;
      this.updateTableData();
    },
    submitDelete() {
      console.log(this.deletingId)
      console.log(this.value[0])
      axios.post(
        'http://localhost:8080/exp/removeExpByOutcomeId',
        { id: this.deletingId }, // 这是请求体
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`
          }
        }
      )
        .then(response => {
          if (response.status === 200) {
            alert('删除成功');
            this.fetchData();
            this.deletedialogVisible = false;
          }
        })


    },


    handleDelete(id) {
      this.deletedialogVisible = true;
      this.deletingId = id;
    },
    searchSubmit() {
      let type = this.value[0];
      this.fullData = this.originalData.filter(item => item['type'] === type);
      this.total = this.fullData.length;  // ✅ 设置总条数
      this.currentPage = 1;
      this.updateTableData();
    },

  },
  mounted() {
    this.fetchData();
  }
};
</script>

<style scoped>
.main-container {
  height: 100vh;
  /* Ensure the container takes the full viewport height */
  width: 100vw;
  /* Ensure the container takes the full viewport width */
  background-color: #dedee0;
  margin: 0;
  /* Ensure no margin */
  padding: 0;
  /* Ensure no padding */
}

.display-layout {
  display: flex;
  height: 100%;
  width: 100%;
}

.el-card {
  width: 100%;
  height: 100%;
}

.card-container {
  padding: 10px;
  height: 100%;
  width: 100%;
  align-items: center;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  /* Align items at the top */
}

.el-pagination {
  margin-top: 20px;
  /* Push the pagination to the bottom */
  margin-bottom: 20px;
  /* Add some space at the bottom */
  display: flex;
  justify-content: center;
  /* Center the pagination */
  width: 100%;
  /* Ensure the pagination takes full width */
}

.header-select {
  display: flex;
  align-items: center;
  /* Center vertically */
  justify-content: space-between;
  /* Ensure items are spaced properly */
  width: 100%;
  /* Ensure it takes full width */
  gap: 10px
}

.blank {
  flex-grow: 1;
  /* Allow blank to take up remaining space */
}
</style>