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
            <el-input v-model="input" style="width: 240px" placeholder="输入关键词" />
            <el-button @click="searchSubmit">搜索</el-button>
          </div>
          <el-table :data="tableData" style="width: 100%">
            <!-- 动态列渲染 -->
            <el-table-column v-for="col in tableColumns" :key="col.prop" :prop="col.prop" :label="col.label" />

            <!-- 固定操作列 -->
            <el-table-column label="Operations" fixed="right" width="150">
              <template #default="scope">
                <el-button link type="primary" size="small" @click="handleClick(scope.row.id)"
                  :disabled="scope.row.account === 'admin'">
                  Edit
                </el-button>
                <el-button link type="danger" size="small" @Click="handleDelete(scope.row.id)"
                  :disabled="scope.row.account === 'admin'">Delete</el-button>
              </template>
            </el-table-column>
          </el-table>
          <el-pagination background layout="prev, pager, next" :total="total" :page-size="pageSize"
            :current-page="currentPage" @current-change="handlePageChange" />
          <!-- 编辑弹窗 -->
          <el-dialog v-model="dialogVisible" title="Edit Row" width="400px">
            <el-form :model="editForm" label-width="100px">
              <el-form-item v-for="col in tableColumns" :key="col.prop" :label="col.label" style="margin-bottom: 12px;">
                <div style="display: flex; gap: 8px; align-items: center">
                  <el-input v-model="editForm[col.prop]" :disabled=editDisabledMap[col.prop] />
                  <el-button @click="startEdit(col.prop)">Edit</el-button>
                </div>
              </el-form-item>
            </el-form>
            <template #footer>
              <el-button @click="dialogVisible = false">Cancel</el-button>
              <el-button type="primary" @click="submitEdit">Save</el-button>
            </template>
          </el-dialog>
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
      tableName: '',
      colName: '',
      searchName: '',
      fullData: [],
      tableData: [],       // 后端数据
      tableColumns: [],
      editForm: [],
      deletingId: '',
      value: ['user'],
      currentPage: 1,      // 当前页码
      pageSize: 10,        // 每页条数
      total: 0,
      dialogVisible: false,
      editDisabledMap: {},
      input: '',
      deletedialogVisible: false,
      options: [{
        value: 'user',
        label: 'user',
        children: [
          {
            value: 'id',
            label: 'id'
          },
          {
            value: 'username',
            label: 'username'
          },
          {
            value: 'password',
            label: 'password'
          },
          {
            value: 'email',
            label: 'email'
          },
          {
            value: 'role',
            label: 'role'
          },
          {
            value: 'all',
            label: 'all'
          }
        ]
      },
      {
        value: 'role',
        label: 'role',
        children: [
          {
            value: 'id',
            label: 'id'
          },
          {
            value: 'account',
            label: 'account'
          },
          {
            value: 'role',
            label: 'role'
          },
          {
            value: 'all',
            label: 'all'
          }
        ]
      }, {
        value: 'outcome',
        label: 'outcome',
        children: [
          {
            value: 'id',
            label: 'id'
          },
          {
            value: 'type',
            label: 'type'
          },
          {
            value: 'args',
            label: 'args'
          },
          {
            value: 'evaluation',
            label: 'evaluation'
          },
          {
            value: 'all',
            label: 'all'
          }
        ]
      }, {
        value: 'experiment',
        label: 'experiment',
        children: [
          {
            value: 'id',
            label: 'id'
          },
          {
            value: 'user_account',
            label: 'user_account'
          },
          {
            value: 'outcome_id',
            label: 'outcome_id'
          },
          {
            value: 'date',
            label: 'date'
          },
          {
            value: 'all',
            label: 'all'
          }
        ]
      },{
        value : 'outcome_dataset',
        label : 'outcome_dataset',
        children: [
          {
            value: 'id',
            label: 'id'
          },
          {
            value: 'outcome_id',
            label: 'outcome_id'
          },
          {
            value: 'dataset_type',
            label: 'dataset_type'
          },
          {
            value : 'all',
            label : 'all'
          },
        ]
      }
      ]    // 根据数据自动生成
    };
  },
  methods: {
    fetchData(tableName, colName, searchName) {
      axios.get('http://127.0.0.1:8080/all/list', {
        params: {
          table: tableName,
          col: colName,
          key: searchName
        },
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`
        }
      }).then((response) => {
        this.fullData = response.data; // 保存所有数据
        console.log(response)
        this.total = this.fullData.length; // 更新总数
        if (tableName == 'user' || tableName == 'role') this.pageSize = 18;
        else if (tableName == 'outcome') this.pageSize = 6;
        this.currentPage = 1; // 回到第一页
        this.updateTableData(); // 刷新当前页数据

        if (this.fullData.length > 0) {
          this.tableColumns = Object.keys(this.fullData[0]).map(key => ({
            prop: key,
            label: key.charAt(0).toUpperCase() + key.slice(1)
          }));
        }
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
      axios.post('http://localhost:8080/all/delete',
        {
          table: this.value[0],
          id: this.deletingId
        },
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`
          }
        }
      ).then(response => {
        if (response.status === 200) {
          alert('删除成功');
          this.fetchData('user');  // 删除后重新获取
          this.deletedialogVisible = false;
        } else {
          alert('删除失败');
        }
      });

    },
    submitEdit() {
      console.log(this.editForm);
      let params = {
        ...this.editForm,
        table: this.value[0],
      };
      axios.post('http://localhost:8080/all/update',
        params,
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`
          }
        }
      ).then(response => {
        if (response.status === 200) {
          alert('修改成功');
          this.fetchData('user');  // 修改后重新获取
          this.dialogVisible = false;
        }
      })
    },


    handleClick(id) {
      this.dialogVisible = true;
      // 清空 editForm 和 editDisabledMap
      this.editForm = {};
      this.editDisabledMap = {};

      const selected = this.tableData.find(item => item.id === id);
      if (selected) {
        // 深拷贝避免联动修改
        this.editForm = JSON.parse(JSON.stringify(selected));
        // 所有字段默认禁用
        for (let key in this.editForm) {
          this.editDisabledMap[key] = true;
        }
      }
    },

    handleDelete(id) {
      this.deletedialogVisible = true;
      this.deletingId = id;
    },
    startEdit(prop) {
      this.editDisabledMap[prop] = false;
    },
    searchSubmit() {
      this.fetchData(this.value[0], this.value[1], this.input);
      console.log(this.tableData)
    }
  },
  mounted() {
    this.fetchData('user');
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