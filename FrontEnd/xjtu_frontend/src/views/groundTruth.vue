<template>
  <div class="main-container">
    <div class="display-layout">
      <!-- 左侧边栏 -->
      <el-aside width="200px">
        <Sidebar />
      </el-aside>
      <!-- 右侧内容区域 -->
      <el-main>
        <div ref="chart" style="width: 100%; height: 100%;"></div>
      </el-main>
    </div>
  </div>
</template>

<script>
import Sidebar from '../components/SideBar.vue';
import * as neo4j from 'neo4j-driver';
import * as echarts from 'echarts';
import axios from 'axios'; // 导入 axios

export default {
  components: {
    Sidebar // Register the Sidebar component
  },
  data() {
    return {
      chart: null,
      graphData: {
        nodes: [],
        links: []
      },
      backendData: [],// 新增属性用于存储后端返回的二维数组
      sourceNode : [],
      targetNode : [],
      alignmentNode : [],
      alignmentLink : []
    };
  },
  mounted() {
    this.initNeo4j().then(() => {
      this.fetchDataFromBackend();
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
            this.graphData.nodes.push({ id: node1Id, name: node1.properties.id.toNumber() || node1Id , type : node1.properties.type });
            if(node1.properties.type === '网络1'){
              this.sourceNode.push(node1);
            }else if(node1.properties.type === '网络2'){
              this.targetNode.push(node1);
            }

            // 添加边
            // this.graphData.links.push({
            //   source: node1Id.toString(),
            //   target: node2Id.toString(),
            //   label: relationship.properties.type || ''
            // });
          });
          session.close();
          driver.close();
        })
        .catch(error => {
          console.error(error);
        });
    },
    initChart() {
      console.log(this.alignmentLink);
      this.chart = echarts.init(this.$refs.chart);

      // 定义节点类型到颜色的映射
      const typeColorMap = {
        '网络1': 'blue',
        '网络2': 'green',
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
              return `节点 ID: ${params.data.properties.id.low}<br/>节点类型: ${params.data.properties.type}<br/>节点名称 : ${params.data.name}`;
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
            layout: 'force',
            data: this.alignmentNode.map(node => ({
              ...node,
              x: null,
              y: null,
              itemStyle: {
                color: typeColorMap[node.properties.type] || 'gray' // 根据类型设置颜色，默认为灰色
              }
            })),
            links: this.alignmentLink,
            categories: [],
            roam: true,
            force: {
              repulsion: 100
            },
            lineStyle: {
              opacity: 0.9,
              width: 2,
              curveness: 0
            },
            edgeSymbol: ['none', 'none'] // 添加箭头表示有向图
          }
        ]
      };
      this.chart.setOption(option);
    },
    fetchDataFromBackend() { // 新增方法
      axios.get('http://localhost:8080/neo4j/doubanGT')
        .then(response => {
          const data = response.data;
          if (data) {
            this.backendData = data; // 存储二维数组
            for(let i = 0; i < this.backendData[0].length; i++){
              let id = this.backendData[0][i];
              for(let j = 0; j < this.sourceNode.length; j++){
                if(this.sourceNode[j].properties.id.low === id) {
                  this.alignmentNode.push(this.sourceNode[j]);
                }
              }
            }
            const len = this.alignmentNode.length;
            for(let i = 0; i < this.backendData[1].length; i++){
              let id = this.backendData[1][i];
              for(let j = 0; j < this.targetNode.length; j++){
                if(this.targetNode[j].properties.id.low === id) this.alignmentNode.push(this.targetNode[j]);
              }
            }
            console.log(this.targetNode.length);
            console.log(this.alignmentNode.length);
            for(let i = len; i < this.alignmentNode.length; i++){
              this.alignmentLink.push({
                source: this.alignmentNode[i-len].properties.id.low,
                target: this.alignmentNode[i].properties.id.low,
                label: 'aligned'
              });
            }
            
            this.initChart();
          } else {
            console.warn("No valid data returned from the backend.");
          }
        })
        .catch(error => {
          console.error("Error fetching data from backend:", error);
        });
    }
  }
}
</script>

<style scoped>
.main-container {
  height: 100vh; /* Ensure the container takes the full viewport height */
  width: 100vw; /* Ensure the container takes the full viewport width */
  background-color: #f7f7f8;
  margin: 0; /* Ensure no margin */
  padding: 0; /* Ensure no padding */
}

.display-layout { 
  display: flex;
  height: 100%;
  width: 100%;
}

.el-main {
  padding: 20px;
}
</style>