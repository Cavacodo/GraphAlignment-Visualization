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
            <a-select v-model:value="SelecteDataset" placeholder="选择数据集" style="width: 120px"
              class="cascade!rounded-button">
              <a-select-option v-for="dataset in datasets" :key="dataset" :value="dataset">
                {{ dataset }}
              </a-select-option>
            </a-select>
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
      SelecteDataset: null,
      nodeId: '',
      types: ['网络1', '网络2'],
      datasets: ['douban', 'ppi'],
      algorithms: ['IsoRank', 'REGAL', 'DeepLink', 'BigAlign', 'FINAL', 'GAlign', 'GTCAlign', 'GroundTruth'],
      algorithms2: ['IsoRank', 'REGAL', 'DeepLink', 'BigAlign', 'FINAL', 'GTCAlign', 'GroundTruth'],
      kValues: [1, 2, 3, 4, 5],
      params: {},
      isDisabled: true,
      chartTitle: "GroundTruth Data"
    };
  },
  watch: {
    SelecteDataset(newDataset) {
      if (newDataset === 'ppi') {
        this.algorithms = this.algorithms.filter(algorithm => algorithm !== 'GAlign');
      } else {
        this.algorithms = this.algorithms;
      }
    },
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
      this.fetchDataFromBackend("douban", 0, 3, 5, false, []);
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
      const dataset = this.SelecteDataset;
      this.clearGraphData();
      if (this.selectedAlgorithm != 'GroundTruth') {
        const result = this.args[this.selectedAlgorithm]
          .filter(item => item.value !== null && item.value !== undefined)
          .map(item => `--${item.label} ${item.value}`).join(' ');
        this.sendInfo(result);
        axios.get('http://localhost:8080/api/getPythonResult', {
          headers: {
            Authorization: 'Bearer ' + localStorage.getItem('token'),
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
          this.fetchDataFromBackend(dataset, type_, this.selectedKValue, this.nodeId, true, m_);
        }).finally(() => {
          this.loading = false;
          this.isDisabled = false;
        });
      } else {
        this.fetchDataFromBackend(dataset, type_, this.selectedKValue, this.nodeId, false, []);
        this.loading = false;
      }
      this.clearArgs();
    },
    sendInfo(result) {
      axios.post('http://localhost:8080/api/send', {
        dataset: this.SelecteDataset == '' ? 'douban' : this.SelecteDataset,
        type: this.selectedAlgorithm,
        args: result,
        user: localStorage.getItem('user'),
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
    fetchDataFromBackend(dataset, type, k, id, isLinked, newAlign) {
      axios.get('http://localhost:8080/neo4j/doubanNetWork', {
        params: { dataset, type, k, id },
        headers: {
          Authorization: `Bearer ` + localStorage.getItem('token'),
        },
        withCredentials: true,
      }).then(response => {
        this.backendData = response.data;
        this.sourceNode = this.backendData.src_node;
        this.targetNode = this.backendData.target_node;
        const prefix1 = type === 0 ? '网络1 ' : '网络2 ';
        const prefix2 = type === 0 ? '网络2 ' : '网络1 ';

        // 内部边
        for (const [from, to] of this.backendData.src) {
          this.alignmentLink.push({
            source: prefix1 + from,
            target: prefix1 + to,
            label: "internal",
            lineStyle: { opacity: 0.5, width: 2, curveness: 0 }
          });
        }
        for (const [from, to] of this.backendData.target) {
          this.alignmentLink.push({
            source: prefix2 + from,
            target: prefix2 + to,
            label: "internal",
            lineStyle: { opacity: 0.5, width: 2, curveness: 0 }
          });
        }

        // 对齐边
        if (isLinked) {
          this.backendData.align = newAlign;
        }
        for (const pair of this.backendData.align) {
          this.alignmentLink.push({
            source: prefix1 + pair[1 - type],
            target: prefix2 + pair[type],
            label: "align",
            lineStyle: { opacity: 0.3,type: 'dashed', width: 2, curveness: 0 }
          });
        }

        const computeForceLayout = (nodes, edges, center, radius = 130, iterations = 300) => {
          const k = 0; // 弹簧理想长度
          const repulsion = 1000; // 排斥力系数
          const damping = 0.6; // 阻尼系数，防止振荡

          // 初始化：随机分布在圆内
          const result = nodes.map(id => {
            const theta = Math.random() * 2 * Math.PI;
            const r = Math.sqrt(Math.random()) * radius; // 均匀分布在圆内
            return {
              rawId: id,
              x: r * Math.cos(theta),
              y: r * Math.sin(theta),
              vx: 0,
              vy: 0,
              fx: 0,
              fy: 0
            };
          });

          for (let iter = 0; iter < iterations; iter++) {
            // 重置力
            for (const n of result) {
              n.fx = 0;
              n.fy = 0;
            }

            // 计算排斥力
            for (let i = 0; i < result.length; i++) {
              for (let j = i + 1; j < result.length; j++) {
                const n1 = result[i], n2 = result[j];
                const dx = n1.x - n2.x;
                const dy = n1.y - n2.y;
                const dist = Math.sqrt(dx * dx + dy * dy) + 0.01;
                const force = repulsion / (dist * dist);
                const fx = force * dx / dist;
                const fy = force * dy / dist;
                n1.fx += fx; n1.fy += fy;
                n2.fx -= fx; n2.fy -= fy;
              }
            }

            // 计算吸引力（边）
            for (const [a, b] of edges) {
              const n1 = result.find(n => n.rawId === a);
              const n2 = result.find(n => n.rawId === b);
              if (!n1 || !n2) continue;
              const dx = n1.x - n2.x;
              const dy = n1.y - n2.y;
              const dist = Math.sqrt(dx * dx + dy * dy) + 0.01;
              const force = (dist - k) * 0.1;
              const fx = force * dx / dist;
              const fy = force * dy / dist;
              n1.fx -= fx; n1.fy -= fy;
              n2.fx += fx; n2.fy += fy;
            }

            // 更新速度和位置，加入阻尼，限制最大移动量
            for (const n of result) {
              n.vx = (n.vx + n.fx) * damping;
              n.vy = (n.vy + n.fy) * damping;

              // 限制单步最大移动，避免震荡过大
              n.vx = Math.max(-10, Math.min(10, n.vx));
              n.vy = Math.max(-10, Math.min(10, n.vy));

              n.x += n.vx;
              n.y += n.vy;

              // 限制节点不超出圆范围
              const distToOrigin = Math.sqrt(n.x * n.x + n.y * n.y);
              if (distToOrigin > radius) {
                const scale = radius / distToOrigin;
                n.x *= scale;
                n.y *= scale;
                // 同时减缓速度避免节点反弹
                n.vx *= 0.5;
                n.vy *= 0.5;
              }
            }
          }

          // 平移到圆心
          for (const n of result) {
            n.x += center.x;
            n.y += center.y;
          }

          return result;
        };



        const layout1 = computeForceLayout(
          type === 0 ? this.sourceNode : this.targetNode,
          type === 0 ? this.backendData.src : this.backendData.target,
          { x: 300, y: 300 }, 130
        );

        const layout2 = computeForceLayout(
          type === 0 ? this.targetNode : this.sourceNode,
          type === 0 ? this.backendData.target : this.backendData.src,
          { x: 700, y: 300 }, 130
        );

        for (const node of layout1) {
          this.alignmentNode.push({
            id: '网络1 ' + node.rawId,
            type: '网络1',
            name: node.rawId,
            x: node.x,
            y: node.y
          });
        }
        for (const node of layout2) {
          this.alignmentNode.push({
            id: '网络2 ' + node.rawId,
            type: '网络2',
            name: node.rawId,
            x: node.x,
            y: node.y
          });
        }

        for (const node of this.alignmentNode) {
          const tmp = type === 0 ? '网络1' : '网络2';
          if (node.type === tmp && node.name == id) {
            node.type = '中心点';
          }
        }

        this.initChart();
      }).catch(error => {
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
  display: flex;
  justify-content: flex-end;
  /* 水平靠右 */
  align-items: flex-start;
  /* 垂直靠上 */
  flex-wrap: nowrap;
  /* 不换行 */
  gap: 0;
  /* 移除间隙 */
  padding: 0;
  /* 移除内边距 */
  margin: 0;
  /* 移除外边距 */
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
