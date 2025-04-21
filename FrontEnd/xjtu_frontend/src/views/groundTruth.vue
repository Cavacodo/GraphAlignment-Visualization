//TODO 本页面
<template>
  <div class="main-container">
    <div class="display-layout">
      <!-- 左侧边栏 -->
      <el-aside width="200px">
        <Sidebar />
      </el-aside>
      <!-- 右侧内容区域 -->
      <el-main style="height: 100%;">
          <el-card>
            <div ref="chart" class="chart-container"></div>
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
      chart: null,
      graphData: {
        nodes: [],
        links: []
      },
      backendData: [],// 新增属性用于存储后端返回的二维数组
      sourceNode: [],
      targetNode: [],
      alignmentNode: [],
      alignmentLink: []
    };
  },
  mounted() {
    this.initNeo4j().then(() => {
      this.fetchDataFromBackend(0, 3, 5);

    });
  },
  methods: {
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
          text: 'GroundTruth Data'
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
            roam: true,
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
    fetchDataFromBackend(type, k, id) {
      axios.get('http://localhost:8080/neo4j/doubanNetWork', {
        params: {
          type: type,
          k: k,
          id: id
        }
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
            if (this.alignmentNode[i].type === tmp && this.alignmentNode[i].name === id) {
              this.alignmentNode[i].type = '中心点';
            }
          }
          this.initChart();
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
.el-card{
  height: 100%;
}
.chart-container{
  width: 100%;
  height: 900px;
}
</style>