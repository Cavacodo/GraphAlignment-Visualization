<template>
  <div class="main-container">
    <div class="display-layout">
      <el-aside width="200px">
        <SideBar />
      </el-aside>
      <div class="card-container">
        <el-card class="card accuarcy">
          <div ref="accuracy" style="width: 100%; height: 100%"></div>
        </el-card>
        <el-card class="card map">
          <div ref="map" style="width: 100%; height: 100%"></div>
          <el-button 
              icon="el-icon-refresh" 
              style="position: absolute; top: 10px; right: 10px; margin: 5px;"
              @click="refreshMap">
              {{text}}
            </el-button>
        </el-card>
        <el-card class="card precision_5">
          <div ref="precision5" style="width: 100%; height: 100%"></div>
        </el-card>
        <el-card class="card precision_10">
          <div ref="precision10" style="width: 100%; height: 100%"></div>
        </el-card>
      </div>
    </div>
  </div>
</template>

<script>
import SideBar from '../components/SideBar.vue';
import * as echarts from 'echarts';
import axios from 'axios';
import { Grid } from 'ant-design-vue';
import { Bottom } from '@element-plus/icons-vue';
export default {
  components: {
    SideBar,
  },
  data() {
    return {
      accuracy: null,
      map: null,
      precision5: null,
      precision10: null,
      text : '切换ppi',
      dataset : 'douban'
    };
  },
  mounted() {
    this.initCharts();
  },
  methods: {
    initCharts() {
      if(this.accuracy != null) this.accuracy.dispose();
      if(this.map != null) this.map.dispose();
      if(this.precision5 != null) this.precision5.dispose();
      if(this.precision10 != null) this.precision10.dispose();
      console.log(this.dataset)
      this.initAccuracyChart();
      this.initMapChart();
      this.initPrecision5Chart();
      this.initPrecision10Chart();
    },
    initAccuracyChart() {
      this.accuracy = echarts.init(this.$refs.accuracy);
      const alg = ['IsoRank', 'REGAL', 'DeepLink', 'BigAlign', 'FINAL', 'GAlign', 'GTCAlign'];
      let yAxisArray = {
        'IsoRank': [],
        'REGAL': [],
        'DeepLink': [],
        'BigAlign': [],
        'FINAL': [],
        'GAlign': [],
        'GTCAlign': [],
      };
      let xAxisArray = [];
      axios.post('http://localhost:8080/outcome/getOutcomeByType', {
        user: localStorage.getItem('user'),
        type: 'Accuracy',
        dataset : this.dataset
      },{
        headers : {
          Authorization : 'Bearer ' + localStorage.getItem('token'),
        },
        withCredentials : true,
      }).then(response => {
        console.log(response.data);
        const len = response.data.length;
        for (let i = 0; i < len; i++) {
          xAxisArray.push(i + 1);
        }
        for (let i = 0; i < alg.length; i++) {
          for (let j = 0; j < len; j++) {
            yAxisArray[alg[i]].push(null);
          }
        }
        for (let i = 0; i < len; i++) {
          yAxisArray[response.data[i]['type']][i] = response.data[i]['evaluation'];
        }
        const option = {
          tooltip: {
            trigger: 'item',
            formatter: (params) => {
              // 获取当前点的索引
              const index = params.dataIndex;
              const item = response.data[index];

              return `
              Type: ${item.type}<br/>
              Args: ${item.args}<br/>
              Accuracy: ${item.evaluation}
              `;
            },
            axisPointer: {
              type: 'cross',
              label: {
                backgroundColor: '#6a7985'
              }

            }

          },
          legend: {
            data: ['IsoRank', 'REGAL', 'DeepLink', 'BigAlign', 'FINAL', 'GAlign', 'GTCAlign'],
            top: '10%',
            left: 'center'
          },
          grid: {
            top: '20%',   // 设置网格的上边距
            containLabel: true, // 确保标签不被裁剪
            botton: '0%'
          },
          toolbox: {
            feature: {
              saveAsImage: {}
            }
          },
          title: {
            text: 'Accuracy'
          },
          xAxis: {
            data: xAxisArray
          },
          yAxis: {
            type : 'value',
            min : 0,
            max : 1
          },
          series: [
            {
              name: 'IsoRank',
              data: yAxisArray['IsoRank'],
              type: 'line',
              areaStyle: {},
              connectNulls: true
            },
            {
              name: 'REGAL',
              data: yAxisArray['REGAL'],
              type: 'line',
              areaStyle: {},
              connectNulls: true
            },
            {
              name: 'DeepLink',
              data: yAxisArray['DeepLink'],
              type: 'line',
              areaStyle: {},
              connectNulls: true
            },
            {
              name: 'BigAlign',
              data: yAxisArray['BigAlign'],
              type: 'line',
              areaStyle: {},
              connectNulls: true
            },
            {
              name: 'FINAL',
              data: yAxisArray['FINAL'],
              type: 'line',
              areaStyle: {},
              connectNulls: true
            },
            {
              name: 'GAlign',
              data: yAxisArray['GAlign'],
              type: 'line',
              areaStyle: {},
              connectNulls: true
            },
            {
              name: 'GTCAlign',
              data: yAxisArray['GTCAlign'],
              type: 'line',
              areaStyle: {},
              connectNulls: true
            },
          ]
        };
        this.accuracy.setOption(option);
      })
    },
    initMapChart() {
      this.map = echarts.init(this.$refs.map);
      const alg = ['IsoRank', 'REGAL', 'DeepLink', 'BigAlign', 'FINAL', 'GAlign', 'GTCAlign'];
      let yAxisArray = {
        'IsoRank': [],
        'REGAL': [],
        'DeepLink': [],
        'BigAlign': [],
        'FINAL': [],
        'GAlign': [],
        'GTCAlign': [],
      };
      let xAxisArray = [];
      axios.post('http://localhost:8080/outcome/getOutcomeByType', {
        type: 'MAP',
        user: localStorage.getItem('user'),
        dataset : this.dataset
        },{
          headers : {
            Authorization : 'Bearer ' + localStorage.getItem('token'),
          },
          withCredentials : true,
        }
      ).then(response => {
        const len = response.data.length;
        for (let i = 0; i < len; i++) {
          xAxisArray.push(i + 1);
        }
        for (let i = 0; i < alg.length; i++) {
          for (let j = 0; j < len; j++) {
            yAxisArray[alg[i]].push(null);
          }
        }
        for (let i = 0; i < len; i++) {
          yAxisArray[response.data[i]['type']][i] = response.data[i]['evaluation'];
        }
        const option = {
          tooltip: {
            trigger: 'item',
            formatter: (params) => {
              // 获取当前点的索引
              const index = params.dataIndex;
              const item = response.data[index];

              return `
              Type: ${item.type}<br/>
              Args: ${item.args}<br/>
              MAP: ${item.evaluation}
              `;
            },
            axisPointer: {
              type: 'cross',
              label: {
                backgroundColor: '#6a7985'
              }

            }

          },
          legend: {
            data: ['IsoRank', 'REGAL', 'DeepLink', 'BigAlign', 'FINAL', 'GAlign', 'GTCAlign'],
            top: '10%',
            left: 'center'
          },
          grid: {
            top: '20%',   // 设置网格的上边距
            containLabel: true, // 确保标签不被裁剪
            botton: '0%'
          },
          toolbox: {
            feature: {
              saveAsImage: {}
            }
          },
          title: {
            text: 'MAP'
          },
          xAxis: {
            data: xAxisArray
          },
          yAxis: {
            type : 'value',
            min : 0,
            max : 1
          },
          series: [
            {
              name: 'IsoRank',
              data: yAxisArray['IsoRank'],
              type: 'line',
              areaStyle: {},
              connectNulls: true
            },
            {
              name: 'REGAL',
              data: yAxisArray['REGAL'],
              type: 'line',
              areaStyle: {},
              connectNulls: true
            },
            {
              name: 'DeepLink',
              data: yAxisArray['DeepLink'],
              type: 'line',
              areaStyle: {},
              connectNulls: true
            },
            {
              name: 'BigAlign',
              data: yAxisArray['BigAlign'],
              type: 'line',
              areaStyle: {},
              connectNulls: true
            },
            {
              name: 'FINAL',
              data: yAxisArray['FINAL'],
              type: 'line',
              areaStyle: {},
              connectNulls: true
            },
            {
              name: 'GAlign',
              data: yAxisArray['GAlign'],
              type: 'line',
              areaStyle: {},
              connectNulls: true
            },
            {
              name: 'GTCAlign',
              data: yAxisArray['GTCAlign'],
              type: 'line',
              areaStyle: {},
              connectNulls: true
            },
          ]
        };
        this.map.setOption(option);
      })
    },
    refreshMap(){
      if(this.text == '切换ppi'){
        this.text = '切换douban';
        this.dataset = 'ppi'
      }
      else{
        this.text = '切换ppi';
        this.dataset = 'douban'
      }
      this.initCharts()
    },
    initPrecision5Chart() {
      this.precision5 = echarts.init(this.$refs.precision5);
      const alg = ['IsoRank', 'REGAL', 'DeepLink', 'BigAlign', 'FINAL', 'GAlign', 'GTCAlign'];
      let yAxisArray = {
        'IsoRank': [],
        'REGAL': [],
        'DeepLink': [],
        'BigAlign': [],
        'FINAL': [],
        'GAlign': [],
        'GTCAlign': [],
      };
      let xAxisArray = [];
      axios.post('http://localhost:8080/outcome/getOutcomeByType', {
        type: 'Precision_5',
        user: localStorage.getItem('user'),
        dataset : this.dataset
        },{
          headers : {
            Authorization : 'Bearer ' + localStorage.getItem('token'),
          },
          withCredentials : true,
      }).then(response => {
        const len = response.data.length;
        for (let i = 0; i < len; i++) {
          xAxisArray.push(i + 1);
        }
        for (let i = 0; i < alg.length; i++) {
          for (let j = 0; j < len; j++) {
            yAxisArray[alg[i]].push(null);
          }
        }
        for (let i = 0; i < len; i++) {
          yAxisArray[response.data[i]['type']][i] = response.data[i]['evaluation'];
        }
        const option = {
          tooltip: {
            trigger: 'item',
            formatter: (params) => {
              // 获取当前点的索引
              const index = params.dataIndex;
              const item = response.data[index];

              return `
              Type: ${item.type}<br/>
              Args: ${item.args}<br/>
              Precision@5: ${item.evaluation}
              `;
            },
            axisPointer: {
              type: 'cross',
              label: {
                backgroundColor: '#6a7985'
              }

            }

          },
          legend: {
            data: ['IsoRank', 'REGAL', 'DeepLink', 'BigAlign', 'FINAL', 'GAlign', 'GTCAlign'],
            top : '10%',
            left : 'center'
          },
          grid: {
            top: '20%',   // 设置网格的上边距
            containLabel: true, // 确保标签不被裁剪
            botton : '0%'
          },
          toolbox: {
            feature: {
              saveAsImage: {}
            }
          },
          title: {
            text: 'Precision@5'
          },
          xAxis: {
            data: xAxisArray
          },
          yAxis: {
            type : 'value',
            min : 0,
            max : 1
          },
          series: [
            {
              name: 'IsoRank',
              data: yAxisArray['IsoRank'],
              type: 'line',
              areaStyle: {},
              connectNulls: true
            },
            {
              name: 'REGAL',
              data: yAxisArray['REGAL'],
              type: 'line',
              areaStyle: {},
              connectNulls: true
            },
            {
              name: 'DeepLink',
              data: yAxisArray['DeepLink'],
              type: 'line',
              areaStyle: {},
              connectNulls: true
            },
            {
              name: 'BigAlign',
              data: yAxisArray['BigAlign'],
              type: 'line',
              areaStyle: {},
              connectNulls: true
            },
            {
              name: 'FINAL',
              data: yAxisArray['FINAL'],
              type: 'line',
              areaStyle: {},
              connectNulls: true
            },
            {
              name: 'GAlign',
              data: yAxisArray['GAlign'],
              type: 'line',
              areaStyle: {},
              connectNulls: true
            },
            {
              name: 'GTCAlign',
              data: yAxisArray['GTCAlign'],
              type: 'line',
              areaStyle: {},
              connectNulls: true
            },
          ]
        };
        this.precision5.setOption(option);
      })
    },
    initPrecision10Chart() {
      this.precision10 = echarts.init(this.$refs.precision10);
      const alg = ['IsoRank', 'REGAL', 'DeepLink', 'BigAlign', 'FINAL', 'GAlign', 'GTCAlign'];
      let yAxisArray = {
        'IsoRank': [],
        'REGAL': [],
        'DeepLink': [],
        'BigAlign': [],
        'FINAL': [],
        'GAlign': [],
        'GTCAlign': [],
      };
      let xAxisArray = [];
      axios.post('http://localhost:8080/outcome/getOutcomeByType', {
        type: 'Precision_10',
        user: localStorage.getItem('user'),
        dataset : this.dataset
        },{
          headers : {
            Authorization : 'Bearer ' + localStorage.getItem('token'),
          },
          withCredentials : true,
      }).then(response => {
        const len = response.data.length;
        for (let i = 0; i < len; i++) {
          xAxisArray.push(i + 1);
        }
        for (let i = 0; i < alg.length; i++) {
          for (let j = 0; j < len; j++) {
            yAxisArray[alg[i]].push(null);
          }
        }
        for (let i = 0; i < len; i++) {
          yAxisArray[response.data[i]['type']][i] = response.data[i]['evaluation'];
        }
        const option = {
          tooltip: {
            trigger: 'item',
            formatter: (params) => {
              // 获取当前点的索引
              const index = params.dataIndex;
              const item = response.data[index];

              return `
              Type: ${item.type}<br/>
              Args: ${item.args}<br/>
              Precision@10: ${item.evaluation}
              `;
            },
            axisPointer: {
              type: 'cross',
              label: {
                backgroundColor: '#6a7985'
              }

            }

          },
          legend: {
            data: ['IsoRank', 'REGAL', 'DeepLink', 'BigAlign', 'FINAL', 'GAlign', 'GTCAlign'],
            top : '10%',
            left : 'center'
          },
          grid: {
            top: '20%',   // 设置网格的上边距
            containLabel: true, // 确保标签不被裁剪
            botton : '0%'
          },
          toolbox: {
            feature: {
              saveAsImage: {}
            }
          },
          title: {
            text: 'Precision@10'
          },
          xAxis: {
            data: xAxisArray
          },
          yAxis: {
            type : 'value',
            min : 0,
            max : 1
          },
          series: [
            {
              name: 'IsoRank',
              data: yAxisArray['IsoRank'],
              type: 'line',
              areaStyle: {},
              connectNulls: true
            },
            {
              name: 'REGAL',
              data: yAxisArray['REGAL'],
              type: 'line',
              areaStyle: {},
              connectNulls: true
            },
            {
              name: 'DeepLink',
              data: yAxisArray['DeepLink'],
              type: 'line',
              areaStyle: {},
              connectNulls: true
            },
            {
              name: 'BigAlign',
              data: yAxisArray['BigAlign'],
              type: 'line',
              areaStyle: {},
              connectNulls: true
            },
            {
              name: 'FINAL',
              data: yAxisArray['FINAL'],
              type: 'line',
              areaStyle: {},
              connectNulls: true
            },
            {
              name: 'GAlign',
              data: yAxisArray['GAlign'],
              type: 'line',
              areaStyle: {},
              connectNulls: true
            },
            {
              name: 'GTCAlign',
              data: yAxisArray['GTCAlign'],
              type: 'line',
              areaStyle: {},
              connectNulls: true
            },
          ]
        };
        this.precision10.setOption(option);
      })
    },

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

.card-container {
  padding: 10px;
  /* container 四周留 10px */
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  /* 卡片之间间距为 10px */
  height: 100%;
  width: 100%;
  box-sizing: border-box;
}

.canvas {
  height: 100%;
  width: 100%;
}

.card {
  width: calc(50% - 5px);
  /* 每行两个卡片 + gap */
  height: calc(50% - 5px);
  /* 每列两个卡片 + gap */
  box-sizing: border-box;
}

.card :deep(.el-card__body) {
  padding: 0;
  height: 100%;
}



.trigger-input {
  width: 300px;
  cursor: pointer;
}

.custom-dropdown {
  padding: 10px;
  background: white;
  box-shadow: 0 0 6px rgba(0, 0, 0, 0.1);
  border-radius: 6px;
  width: 300px;
}

.input-group {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}

.label {
  width: 50px;
  text-align: right;
}

.flex-1 {
  margin: 2px;
  width: 100%;
}

.cascade {
  margin-left: 5px;
  margin-right: 5px;
}

:deep(.ant-select-selector) {
  border-radius: 6px !important;
}

:deep(.ant-input-number) {
  width: 100%;
}

:deep(.params-card .ant-card-body) {
  padding: 16px;
}
</style>
