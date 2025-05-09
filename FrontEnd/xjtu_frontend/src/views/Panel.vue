<template>
  <div class="main-container">
    <div class="display-layout">
      <!-- 左侧边栏 -->
      <el-aside width="200px">
        <Sidebar />
      </el-aside>
      <!-- 右侧内容区域 -->
      <el-main style="height: 100%;">
        <el-card class="canvas-container">
          <a-spin v-if="loading" tip="Loading..." class="spin" />
          <div ref="chart" class="chart-container"></div>
          <div class="select-bar">
            <!-- 类型选择器 -->
            <a-select v-model:value="selectedType" placeholder='选择类型' style="width: 120px"
              class="cascade!rounded-button">
              <a-select-option v-for="type in types" :key="type" :value="type">
                {{ type }}
              </a-select-option>
            </a-select>
            <!-- 算法选择器 -->
            <a-select v-model:value="selectedAlgorithm" placeholder="选择算法" style="width: 120px"
              class="cascade !rounded-button">
              <a-select-option v-for="algorithm in algorithms" :key="algorithm" :value="algorithm">
                {{ algorithm }}
              </a-select-option>
            </a-select>
            <!-- K值选择器 -->
            <a-select v-model:value="selectedKValue" placeholder="K值" style="width: 100px"
              class="cascade !rounded-button">
              <a-select-option v-for="k in kValues" :key="k" :value="k">
                {{ k }}
              </a-select-option>
            </a-select>
            <!-- 节点ID输入框 -->
            <a-input v-model:value="nodeId" placeholder="请输入节点ID" class="cascade !rounded-button"
              style="width: 150px" />
            <!-- 参数配置 -->
            <a-dropdown :trigger="['click']" :visible="dropdownVisible" @visibleChange="handleDropdownVisibleChange">
              <a-button class="cascade !rounded-button whitespace-nowrap" style="width: 150px">
                参数设置
                <down-outlined :style="{ fontSize: '12px' }" />
              </a-button>
              <template #overlay>
                <a-card class="params-card" style="width: 150px">
                  <div class="space-y-3" style="display: flex; flex-direction: column; align-items: center;">
                    <div v-for="arg in args[selectedAlgorithm] || []" key="arg.label">
                      <a-input v-if="arg.type === 'number' || arg.type === 'float'" v-model:value="arg.value"
                        :placeholder="arg.placeholder" style="margin-bottom: 8px; width: 130px;" />
                    </div>
                  </div>
                </a-card>
              </template>
            </a-dropdown>
            <a-button :disabled="isDisabled" class="cascade" @click="handleClick">提交</a-button>
          </div>
        </el-card>
        <el-card class="evaluation-container">
          <div class="evaluation-content">
            <el-card class="eva gradient-card">
              <div class="index">Accuracy</div>
              <div class="acc">{{ accuracy }}</div>
            </el-card>
            <el-card class="eva gradient-card">
              <div class="index">MAP</div>
              <div class="map">{{ MAP }}</div>
            </el-card>
            <el-card class="eva gradient-card">
              <div class="index">Presion_5</div>
              <div class="precision_5">{{ precision_5 }}</div>
            </el-card>
            <el-card class="eva gradient-card">
              <div class="index">Presion_10</div>
              <div class="precision_10">{{ precision_10 }}</div>
            </el-card>
            <el-card class="eva gradient-card">
              <div class="index">AUC</div>
              <div class="auc">{{ AUC }}</div>
            </el-card>
          </div>
        </el-card>
      </el-main>
    </div>
  </div>
</template>

<script>
import Sidebar from '../components/SideBar.vue';
import * as neo4j from 'neo4j-driver';
import { Card } from 'ant-design-vue';
import * as echarts from 'echarts';
import axios from 'axios'; // 导入 axios
export default {
  components: {
    Sidebar, // Register the Sidebar component
    Card,// Register the Card component
  },
  data() {
    return {
      dropdownVisible: false,
      chart: null,
      graphData: {
        nodes: [],
        links: []
      },
      backendData: [],// 新增属性用于存储后端返回的二维数组
      sourceNode: [],
      targetNode: [],
      alignmentNode: [],
      alignmentLink: [],
      accuracy: '--%',
      MAP: '--',
      precision_5: '--',
      precision_10: '--',
      AUC: '--',
      loading: false,
      args: {
        'IsoRank': [
          { label: 'max_iter', type: 'number', value: null, placeholder: 'maxIteration' },
          { label: 'alpha', type: 'float', value: null, placeholder: 'alpha' },
          { label: 'tol', type: 'float', value: null, placeholder: 'tol' },
        ],
        'REGAL': [
          { label: 'attrvals', type: 'number', value: null, placeholder: 'attrvals' },
          { label: 'dimensions', type: 'numver', value: null, placeholder: 'dimensions' },
          { label: 'max_layer', type: 'number', value: null, placeholder: 'max_layer' },
          { label: 'k', type: 'number', value: null, placeholder: 'K' },
          { label: 'alpha', type: 'float', value: null, placeholder: 'alpha' },
          { label: 'gammastruc', type: 'float', value: null, placeholder: 'gammastruc' },
          { label: 'gammaattr', type: 'float', value: null, placeholder: 'gammaattr' },
          { label: 'num_top', type: 'number', value: null, placeholder: 'num_top' },
          { label: 'buckets', type: 'float', value: null, placeholder: 'buckets' }
        ],
        'DeepLink': [
          { label: 'embedding_dim', type: 'number', value: null, placeholder: 'embedding_dim' },
          { label: 'embedding_epochs', type: 'number', value: null, placeholder: 'embedding_epochs' },
          { label: 'unsupervised_lr', type: 'float', value: null, placeholder: 'unsupervised_lr' },
          { label: 'supervised_lr', type: 'float', value: null, placeholder: 'supervised_lr' },
          { label: 'batch_size_mapping', type: 'number', value: null, placeholder: 'batch_size_mapping' },
          { label: 'unsupervised_epochs', type: 'number', value: null, placeholder: 'unsupervised_epochs' },
          { label: 'supervised_epochs', type: 'number', value: null, placeholder: 'supervised_epochs' },
          { label: 'hidden_dim1', type: 'number', value: null, placeholder: 'hidden_dim1' },
          { label: 'hidden_dim2', type: 'number', value: null, placeholder: 'hidden_dim2' },
          { label: 'number_walks', type: 'number', value: null, placeholder: 'number_walks' },
          { label: 'walk_length', type: 'number', value: null, placeholder: 'walk_length' },
          { label: 'window_size', type: 'number', value: null, placeholder: 'window_size' },
          { label: 'top_k', type: 'number', value: null, placeholder: 'top_k' },
          { label: 'alpha', type: 'float', value: null, placeholder: 'alpha' },
          { label: 'num_cores', type: 'number', value: null, placeholder: 'num_cores' },
        ],
        'BigAlign': [
          { label: 'lamb', type: 'float', value: null, placeholder: 'lamb' },
        ],
        'FINAL': [
          { label: 'max_iter', type: 'number', value: null, placeholder: 'maxIteration' },
          { label: 'alpha', type: 'float', value: null, placeholder: 'alpha' },
          { label: 'tol', type: 'float', value: null, placeholder: 'tol' },
        ],
        'GAlign': [
          { label: 'embedding_dim', type: 'number', value: null, placeholder: 'embedding_dim' },
          { label: 'GAlign_epochs', type: 'number', value: null, placeholder: 'GAlign_epochs' },
          { label: 'lr', type: 'float', value: null, placeholder: 'lr' },
          { label: 'num_GCN_blocks', type: 'number', value: null, placeholder: 'num_GCN_blocks' },
          { label: 'alpha0', type: 'float', value: null, placeholder: 'alpha0' },
          { label: 'alpha1', type: 'float', value: null, placeholder: 'alpha1' },
          { label: 'alpha2', type: 'float', value: null, placeholder: 'alpha2' },
          { label: 'noise_level', type: 'float', value: null, placeholder: 'noise_level' },
          { label: 'refinement_epochs', type: 'number', value: null, placeholder: 'refinement_epochs' },
          { label: 'threshold_refine', type: 'float', value: null, placeholder: 'threshold_refine' },
          { label: 'beta', type: 'float', value: null, placeholder: 'beta' },
          { label: 'threshold', type: 'float', value: null, placeholder: 'threshold' },
          { label: 'coe_consistency', type: 'float', value: null, placeholder: 'coe_consistency' },
        ],
        'GTCAlign': [
          { label: 'alpha', type: 'float', value: null, placeholder: 'alpha' },
          { label: 'gcn_block', type: 'number', value: null, placeholder: 'gcn_block' },
          { label: 'output_dim', type: 'number', value: null, placeholder: 'output_dim' },
          { label: 'r_epochs', type: 'number', value: null, placeholder: 'r_epochs' },
          { label: 'top_k', type: 'number', value: null, placeholder: 'top_k' }
        ]
      },
      selectedType: null,
      selectedAlgorithm: null,
      selectedKValue: null,
      nodeId: '',
      types: ['网络1', '网络2'],
      algorithms: ['IsoRank', 'REGAL', 'DeepLink', 'BigAlign', 'FINAL', 'GAlign', 'GTCAlign', 'GroundTruth'],
      kValues: [1, 2, 3, 4, 5],
      params: {},
      isDisabled: true,
      chartTitle: "GroundTruth Data"
    };
  },
  watch: {
    selectedType() {
      this.checkIntegrity();
    },
    selectedKValue() {
      this.checkIntegrity();
    },
    selectedAlgorithm() {
      this.checkIntegrity();

    },
    nodeId() {
      this.checkIntegrity();
    },
  },
  mounted() {
    this.initNeo4j().then(() => {
      this.fetchDataFromBackend(0, 3, 5, false, []);
    });
  },

  methods: {
    handleDropdownVisibleChange(visible) {
      this.dropdownVisible = visible;
    },
    clearArgs() {
      for (const algorithm in this.args) {
        if (Array.isArray(this.args[algorithm])) {
          this.args[algorithm].forEach(arg => {
            arg.value = null;
          });
        }
      }
    },
    checkIntegrity() {
      if (this.selectedType && this.selectedKValue && this.selectedAlgorithm && this.nodeId) {
        this.isDisabled = false;
      }
    },
    handleClick() {
      this.loading = true;
      this.isDisabled = true;
      let m_ = null;
      const type_ = this.selectedType === '网络1' ? 0 : 1;
      this.clearGraphData();
      if (this.selectedAlgorithm != 'GroundTruth') {
        const result = this.args[this.selectedAlgorithm]
          .filter(item => item.value !== null && item.value !== undefined)
          .map(item => `--${item.label} ${item.value}`).join(' ');
        this.sendInfo(result);
        axios.get('http://localhost:8080/api/getPythonResult', {
          headers:{
            Authorization : 'Bearer ' + localStorage.getItem('token'),
          },
          withCredentials: true,
        }).then(response => {
          this.accuracy = response.data.acc["'Accuracy'"].trim().replace(/^'(.*)'$/, '$1').trim();
          this.MAP = response.data.acc[" 'MAP'"].trim().replace(/^'(.*)'$/, '$1').trim();
          this.AUC = response.data.acc[" 'AUC'"].trim().replace(/^'(.*)'$/, '$1').trim();
          this.precision_5 = response.data.acc[" 'Precision_5'"].trim().replace(/^'(.*)'$/, '$1').trim();
          this.precision_10 = response.data.acc[" 'Precision_10'"].trim().replace(/^'(.*)'$/, '$1').trim();
          m_ = response.data.m;
        }).then(() => {
          this.chartTitle = this.selectedAlgorithm;
          this.fetchDataFromBackend(type_, this.selectedKValue, this.nodeId, true, m_);
        }).finally(() => {
          this.loading = false;
          this.isDisabled = false;
        });
      } else {
        this.fetchDataFromBackend(type_, this.selectedKValue, this.nodeId, false, []);
        this.loading = false;
      }
      this.clearArgs();
    },
    sendInfo(result) {
      axios.post('http://localhost:8080/api/send', {
        type: this.selectedAlgorithm,
        args: result
      },
      {
        withCredentials: true,
        headers: {
          Authorization: 'Bearer ' + localStorage.getItem('token')
        }
      })
    },
    initNeo4j() {
      const driver = neo4j.driver('bolt://localhost:7687', neo4j.auth.basic('neo4j', 'neo4jpassword'));
      const session = driver.session();

      // 更新查询语句
      const query = `
        MATCH (n)
        RETURN n
        `;
      return session
        .run(query)
        .then((result) => {
          if (result.records.length === 0) {
            console.warn("No data returned from the query.");
            return;
          }
          result.records.forEach((record) => {
            const node1 = record.get('n');
            // 确保节点有 id 属性
            const node1Id = node1.properties.id.toNumber();
            this.graphData.nodes.push({ id: node1.properties.type + ' ' + node1.properties.id.toNumber(), name: node1Id || node1Id, type: node1.properties.type });

          });
          session.close();
          driver.close();
        })
        .catch(error => {
          console.error(error);
        });
    },
    initChart() {
      this.chart = echarts.init(this.$refs.chart);

      // 定义节点类型到颜色的映射
      const typeColorMap = {
        '网络1': 'blue',
        '网络2': 'green',
        '中心点': 'red'
        // 可以根据需要添加更多类型和颜色
      };

      const option = {
        title: {
          text: this.chartTitle
        },
        tooltip: {
          trigger: 'item',
          formatter: (params) => {
            if (params.dataType === 'node') {
              return `节点 ID: ${params.data.id}<br/>节点类型: ${params.data.type}<br/>节点名称 : ${params.data.name}`;
            } else if (params.dataType === 'edge') {
              return `边：${params.data.source} -> ${params.data.target}`;
            }
            return '';
          },
        },
        label: {
          show: true,
          formatter: (params) => {
            return params.data.properties.id.low; // 显示节点 ID
          }
        },
        series: [
          {
            type: 'graph',
            layout: 'none',
            data: this.alignmentNode.map(node => ({
              ...node,
              itemStyle: {
                color: typeColorMap[node.type] || 'gray', // 根据类型设置颜色，默认为灰色
                borderColor: 'black', // 边框颜色
                borderWidth: 1, // 边框宽度
              }
            })),
            links: this.alignmentLink,
            categories: [

            ],
            roam: false,
            force: {
              repulsion: 100,
            },
            edgeLabel: {
              show: false, // 关键：必须声明默认结构
              formatter: () => ''
            },
            emphasis: {
              lineStyle: {
                opacity: 1,  // 悬停时显示线
                color: '#f00'
              }
            },
            edgeSymbol: ['none', 'none'] // 添加箭头表示有向图
          }
        ]
      };
      this.chart.setOption(option);
    },
    clearGraphData() {
      this.backendData = [];
      this.sourceNode = [];
      this.targetNode = [];
      this.alignmentNode = [];
      this.alignmentLink = [];
    },
    fetchDataFromBackend(type, k, id, isLinked, newAlign) {
      axios.get('http://localhost:8080/neo4j/doubanNetWork', {
        params: {
          type: type,
          k: k,
          id: id
        }, headers: {
          Authorization: `Bearer ` + localStorage.getItem('token'),
        },
        withCredentials:true,
      }) // 替换为实际的后端 API 地址
        .then(response => {
          this.backendData = response.data;
          this.sourceNode = this.backendData.src_node;
          this.targetNode = this.backendData.target_node;
          var prefix1 = type === 0 ? '网络1 ' : '网络2 ';
          var prefix2 = type === 0 ? '网络2 ' : '网络1 ';
          for (var i = 0; i < this.backendData.src.length; i++) {
            this.alignmentLink.push({
              source: prefix1 + this.backendData.src[i][0],
              target: prefix1 + this.backendData.src[i][1],
              label: "internal",
              lineStyle: {
                opacity: 0.5,
                width: 2,
                curveness: 0
              }
            });
          }
          for (var i = 0; i < this.backendData.target.length; i++) {
            this.alignmentLink.push({
              source: prefix2 + this.backendData.target[i][0],
              target: prefix2 + this.backendData.target[i][1],
              label: "internal",
              lineStyle: {
                opacity: 0.5,
                width: 2,
                curveness: 0
              }
            });
          }
          if (isLinked) {
            this.backendData.align = newAlign;
          }
          for (var i = 0; i < this.backendData.align.length; i++) {
            this.alignmentLink.push({
              source: prefix1 + this.backendData.align[i][1 - type],
              target: prefix2 + this.backendData.align[i][type],
              label: "align",
              lineStyle: {
                opacity: 0,
                width: 2,
                curveness: 0
              }
            });
          }
          var radius = 120;
          if (type === 0) {
            for (var i = 0; i < this.sourceNode.length; i++) {
              const theta = Math.random() * 2 * Math.PI;
              const r = Math.sqrt(Math.random()) * radius;
              this.alignmentNode.push({
                id: "网络1 " + this.sourceNode[i],
                type: '网络1',
                name: this.sourceNode[i],
                x: 300 + r * Math.cos(theta),
                y: 300 + r * Math.sin(theta),
              });
            }
            for (var j = 0; j < this.targetNode.length; j++) {
              const theta = Math.random() * 2 * Math.PI;
              const r = Math.sqrt(Math.random()) * radius;
              this.alignmentNode.push({
                id: "网络2 " + this.targetNode[j],
                type: '网络2',
                name: this.targetNode[j],
                x: 700 + r * Math.cos(theta),
                y: 300 + r * Math.sin(theta),
              });
            }
          } else {
            for (var i = 0; i < this.targetNode.length; i++) {
              const theta = Math.random() * 2 * Math.PI;
              const r = Math.sqrt(Math.random()) * radius;
              this.alignmentNode.push({
                id: "网络1 " + this.targetNode[i],
                type: '网络1',
                name: this.targetNode[i],
                x: 300 + r * Math.cos(theta),
                y: 300 + r * Math.sin(theta),
              });
            }
            for (var j = 0; j < this.sourceNode.length; j++) {
              const theta = Math.random() * 2 * Math.PI;
              const r = Math.sqrt(Math.random()) * radius;
              this.alignmentNode.push({
                id: "网络2 " + this.sourceNode[j],
                type: '网络2',
                name: this.sourceNode[j],
                x: 700 + r * Math.cos(theta),
                y: 300 + r * Math.sin(theta),
              })
            }
          }
          for (var i = 0; i < this.alignmentNode.length; i++) {
            var tmp = type === 0 ? '网络1' : '网络2';
            if (this.alignmentNode[i].type === tmp && this.alignmentNode[i].name == id) {
              this.alignmentNode[i].type = '中心点';
            }
          }
          this.initChart()
        })
        .catch(error => {
          console.error('Error fetching data:', error);
        });
    },

  }
}
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

.el-main {
  align-items: center;
  padding: 10px;
}

.canvas-container {
  height: 85%;
  position: relative;
  text-align: center;
}

.spin {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 999;
  display: inline-block;
}

.chart-container {
  width: 100%;
  height: 720px;
  position: absolute;
}

.select-bar {
  display: inline-block;
  position: absolute;
}

.evaluation-container {
  margin-top: 10px;
  padding: 0px;
  height: 13%;
  width: 100%;

}

.evaluation-content {
  display: flex;
  width: 100%;
  display: flex;
  justify-content: center;
}

.gradient-card {
  background: linear-gradient(135deg, #cfe3fa, #accef4);
  /* 渐变蓝色 */
  border: none;
  /* 可选：去掉边框 */
}

.eva {
  margin-left: 2%;
  margin-right: 2%;
  width: 20%;
  height: 70px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  /* 垂直方向居中 */
  align-items: flex-start;
  /* 水平方向靠左 */
}

.acc {
  font-size: 20px;
  font-weight: 800;
  color: #224ead;
}

.map {
  font-size: 20px;
  font-weight: 800;
  color: #224ead;
}

.precision_5 {
  font-size: 20px;
  font-weight: 800;
  color: #224ead;
}

.precision_10 {
  font-size: 20px;
  font-weight: 800;
  color: #224ead;
}

.auc {
  font-size: 20px;
  font-weight: 800;
  color: #224ead;
}

.index {
  font-weight: 600;
  font-size: small;
}
</style>