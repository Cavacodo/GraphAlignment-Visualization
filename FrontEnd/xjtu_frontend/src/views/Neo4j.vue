<template>
  <div class="main-container">
    <el-container>
      <el-aside width="200px">
        <!-- 左侧导航栏内容 -->
        <el-menu default-active="1" class="el-menu-vertical-demo">
          <el-menu-item index="1">
            <i class="el-icon-menu"></i>
            <span slot="title">导航一</span>
          </el-menu-item>
          <el-menu-item index="2">
            <i class="el-icon-document"></i>
            <span slot="title">导航二</span>
          </el-menu-item>
          <el-menu-item index="3">
            <i class="el-icon-setting"></i>
            <span slot="title">导航三</span>
          </el-menu-item>
        </el-menu>
      </el-aside>
      <el-main>
        <div class="g1">
          <el-cascader v-model="value1" :options="options1" @change="handleChange1" style="margin-top: 20px;"/>
          <div ref="neo4jGraph" class="graph-container1"></div>
        </div>
        <div class="g2">
          <el-cascader v-model="value2" :options="options2" @change="handleChange2" style="margin-top: 20px;"/>
          <div ref="neo4jGraph2" class="graph-container2"></div>
        </div> <!-- 添加第二个图表容器 -->
        <el-dialog v-model="dialogTableVisible" title="节点信息" width="800">
          <el-table :data="gridData">
            <el-table-column property="id" label="id" width="150" />
            <el-table-column property="label" label="label" width="200" />
            <el-table-column property="neighbor" label="neighbor" />
            <el-table-column property="align" label="align" width="200" />
          </el-table>
        </el-dialog>
      </el-main>
    </el-container>
  </div>
</template>

<script>
import { reactive, ref } from 'vue'
import neo4j from "neo4j-driver";
import vis from 'vis-network/dist/vis-network.min';
import 'vis-network/styles/vis-network.css'; // 修改后的路径

export default {
  name: "Neo4jGraph",
  data() {
    return {
      nodes: new vis.DataSet([]),
      edges: new vis.DataSet([]),
      nodes2: new vis.DataSet([]), // 添加第二个图表的节点数据集
      edges2: new vis.DataSet([]),  // 添加第二个图表的边数据集
      selectedNode: null, // 选中的节点信息
      dialogTableVisible: false, // 添加 dialogTableVisible 到 data 中
      gridData: [], // 添加 gridData 数组
      value1: [], // 移动 value 到 data 中
      value2: [], // 移动 value 到 data 中
      options1: [ // 移动 options 到 data 中
        { value: '0-300', label: '0-300' },
        { value: '301-600', label: '301-600' },
        { value: '601-900', label: '601-900' },
        { value: '901-1200', label: '901-1200' },
      ],
      options2: [ // 移动 options 到 data 中
        { value: '0-300', label: '0-300' },
        { value: '301-600', label: '301-600' },
        { value: '601-900', label: '601-900' },
        { value: '901-1200', label: '901-1200' },
        { value: '1201-1500', label: '1201-1500' },
        { value: '1501-1800', label: '1501-1800' },
        { value: '1801-2100', label: '1801-2100' },
        { value: '2101-2400', label: '2101-2400' },
        { value: '2401-2700', label: '2401-2700' },
        { value: '2701-3000', label: '2701-3000' },
        { value: '3001-3300', label: '3001-3300' },
        { value: '3301-3600', label: '3301-3600' },
        { value: '3601-3900', label: '3601-3900' },
        { value: '3901-4000', label: '3901-4000' },
      ] // 添加第二个图表的选项
    };
  },
  methods: {
    handleChange1(value) {
      // 将 value 转换为字符串
      const valueStr = Array.isArray(value) ? value.join('-') : value.toString();
      this.fetchData(valueStr, '网络1', this.nodes, this.edges, this.$refs.neo4jGraph);
    },
    handleChange2(value) {
      // 将 value 转换为字符串
      const valueStr = Array.isArray(value) ? value.join('-') : value.toString();
      this.fetchData(valueStr, '网络2', this.nodes2, this.edges2, this.$refs.neo4jGraph2);
    },
    fetchData(value, type, nodes, edges, container) {
      // 清空现有数据
      nodes.clear();
      edges.clear();

      // 初始化 Neo4j 驱动
      const driver = neo4j.driver(
        "bolt://localhost:7687",
        neo4j.auth.basic("neo4j", "neo4jpassword")
      );

      const session = driver.session();

      // 根据选择的值构建查询
      const [minId, maxId] = value.split('-').map(Number);
      console.log(type)
      console.log(minId, maxId)
      const query = `
        MATCH (n)-[r]-(m)
        WHERE n.type = '${type}' AND m.type = '${type}' AND n.id >= ${minId} AND n.id <= ${maxId} AND m.id >= ${minId} AND m.id <= ${maxId}
        RETURN DISTINCT n, r, m
      `;

      session
        .run(query)
        .then((result) => {
          console.log(result.records);
          if (result.records.length === 0) {
            console.warn("No data returned from the query.");
            return;
          }
          result.records.forEach((record) => {
            const node1 = record.get('n');
            const node2 = record.get('m');
            const relationship = record.get('r');

            // 确保节点有 id 属性
            const node1Id = node1.identity.toNumber();
            const node2Id = node2.identity.toNumber();

            // 检查节点ID是否在范围内
            if (node1Id >= minId && node1Id <= maxId) {
              if (!nodes.get(node1Id)) {
                nodes.add({ id: node1Id, label: node1.properties.name || node1Id });
              }
            }
            if (node2Id >= minId && node2Id <= maxId) {
              if (!nodes.get(node2Id)) {
                nodes.add({ id: node2Id, label: node2.properties.name || node2Id });
              }
            }

            // 添加边
            if (nodes.get(node1Id) && nodes.get(node2Id)) {
              edges.add({
                from: node1Id,
                to: node2Id,
                label: relationship.properties.type || ''
              });
            }
          });

          // 创建网络
          const data = {
            nodes: nodes,
            edges: edges
          };
          const options = {
            physics: {
              enabled: false
            },
            edges: {
              arrows: {
                to: { enabled: true } // 添加箭头到目标节点
              }
            }
          };
          const network = new vis.Network(container, data, options);

          // 监听 selectNode 事件
          network.on('selectNode', (params) => {
            if (params.nodes.length > 0) {
              this.dialogTableVisible = true; // 修改为 this.dialogTableVisible
              const nodeId = params.nodes[0];
              const node = nodes.get(nodeId);
              this.selectedNode = node;
              console.log('Selected Node:', node); // 添加调试信息

              // 获取邻居节点
              const neighbors = edges.get({
                filter: function(edge) {
                  return edge.from === nodeId || edge.to === nodeId;
                }
              }).map(edge => {
                return edge.from === nodeId ? edge.to : edge.from;
              }).map(id => nodes.get(id));

              // 填充 gridData 数组
              this.gridData = [{
                id: node.id,
                label: node.label,
                neighbor: neighbors.map(n => n.label).join(', '),
                align: '' // 假设 align 字段为空，可以根据需要填充
              }];
            }
          });
        })
        .catch((error) => {
          console.error("Error executing query:", error);
        })
        .finally(() => {
          session.close();
          driver.close();
        });
    }
  },
  mounted() {
    // 初始化 Neo4j 驱动
    const driver = neo4j.driver(
      "bolt://localhost:7687",
      neo4j.auth.basic("neo4j", "neo4jpassword")
    );

    const session = driver.session();

    // 查询 Neo4j 数据
    const query = `
      MATCH (n)-[r]-(m)
      WHERE n.type = '网络1' AND m.type = '网络1'
      RETURN DISTINCT n, r, m LIMIT 500
    `;
    session
      .run(query)
      .then((result) => {
        if (result.records.length === 0) {
          console.warn("No data returned from the query.");
          return;
        }
        result.records.forEach((record) => {
          const node1 = record.get('n');
          const node2 = record.get('m');
          const relationship = record.get('r');

          // 确保节点有 id 属性
          const node1Id = node1.identity.toNumber();
          const node2Id = node2.identity.toNumber();

          // 添加节点
          if (!this.nodes.get(node1Id)) {
            this.nodes.add({ id: node1Id, label: node1.properties.name || node1Id });
          }
          if (!this.nodes.get(node2Id)) {
            this.nodes.add({ id: node2Id, label: node2.properties.name || node2Id });
          }

          // 添加边
          this.edges.add({
            from: node1Id,
            to: node2Id,
            label: relationship.properties.type || ''
          });
        });

        // 创建第一个网络
        const container = this.$refs.neo4jGraph;
        const data = {
          nodes: this.nodes,
          edges: this.edges
        };
        const options = {
          physics: {
            enabled: false
          },
          edges: {
            arrows: {
              to: { enabled: true } // 添加箭头到目标节点
            }
          }
        };
        const network = new vis.Network(container, data, options);

        // 监听 selectNode 事件
        network.on('selectNode', (params) => {
          if (params.nodes.length > 0) {
            this.dialogTableVisible = true; // 修改为 this.dialogTableVisible
            const nodeId = params.nodes[0];
            const node = this.nodes.get(nodeId);
            this.selectedNode = node;
            console.log('Selected Node:', node); // 添加调试信息

            // 获取邻居节点
            const neighbors = this.edges.get({
              filter: function(edge) {
                return edge.from === nodeId || edge.to === nodeId;
              }
            }).map(edge => {
              return edge.from === nodeId ? edge.to : edge.from;
            }).map(id => this.nodes.get(id));

            // 填充 gridData 数组
            this.gridData = [{
              id: node.id,
              label: node.label,
              neighbor: neighbors.map(n => n.label).join(', '),
              align: '' // 假设 align 字段为空，可以根据需要填充
            }];
          }
        });

        // 查询第二个图表的数据
        const query2 = `
          MATCH (n)-[r]-(m)
          WHERE n.type = '网络2' AND m.type = '网络2'
          RETURN DISTINCT n, r, m LIMIT 500
        `;
        return session.run(query2);
      })
      .then((result2) => {
        if (result2.records.length === 0) {
          console.warn("No data returned from the second query.");
          return;
        }
        result2.records.forEach((record) => {
          const node1 = record.get('n');
          const node2 = record.get('m');
          const relationship = record.get('r');

          // 确保节点有 id 属性
          const node1Id = node1.identity.toNumber();
          const node2Id = node2.identity.toNumber();

          // 添加节点
          if (!this.nodes2.get(node1Id)) {
            this.nodes2.add({ id: node1Id, label: node1.properties.name || node1Id });
          }
          if (!this.nodes2.get(node2Id)) {
            this.nodes2.add({ id: node2Id, label: node2.properties.name || node2Id });
          }

          // 添加边
          this.edges2.add({
            from: node1Id,
            to: node2Id,
            label: relationship.properties.type || ''
          });
        });

        // 创建第二个网络
        const container2 = this.$refs.neo4jGraph2;
        const data2 = {
          nodes: this.nodes2,
          edges: this.edges2
        };
        const options2 = {
          physics: {
            enabled: false
          },
          nodes: {
            color: {
              background: '#8BC34A',
              border: '#333',
              highlight: {
                background: '#66BB6A',
                border: '#2e7d32'
              }
            }
          },
          edges: {
            color: {
              color: '#000', // 红色
              highlight: '#000' // 红色
            },
            arrows: {
              to: { enabled: true } // 添加箭头到目标节点
            }
          }
        };
        const network2 = new vis.Network(container2, data2, options2);

        // 监听 selectNode 事件
        network2.on('selectNode', (params) => {
          if (params.nodes.length > 0) {
            this.dialogTableVisible = true; // 修改为 this.dialogTableVisible
            const nodeId = params.nodes[0];
            const node = this.nodes2.get(nodeId);
            this.selectedNode = node;
            console.log('Selected Node:', node); // 添加调试信息

            // 获取邻居节点
            const neighbors = this.edges2.get({
              filter: function(edge) {
                return edge.from === nodeId || edge.to === nodeId;
              }
            }).map(edge => {
              return edge.from === nodeId ? edge.to : edge.from;
            }).map(id => this.nodes2.get(id));

            // 填充 gridData 数组
            this.gridData = [{
              id: node.id,
              label: node.label,
              neighbor: neighbors.map(n => n.label).join(', '),
              align: '' // 假设 align 字段为空，可以根据需要填充
            }];
          }
        });
      })
      .catch((error) => {
        console.error("Error executing query:", error);
      })
      .finally(() => {
        session.close();
        driver.close();
      });
  },
};
</script>

<style scoped>
:root {
  height: 100%;
  width: 100%;
}

.main-container {
  height: 100%;
  width: 100%;
  position: absolute;
}

.graph-container1, .graph-container2 {
  height: 100%; /* 调整图表容器的高度 */
  width: 100%; /* 调整图表容器的宽度 */
  margin: 0;
  padding: 0;
}

.el-container {
  height: 100vh;
}

.el-aside {
  background-color: #D3DCE6;
  color: #333;
  text-align: center;
  line-height: 200px;
}

.el-main {
  background-color: #E9EEF3;
  color: #333;
  text-align: center;
  margin: 0;
  padding: 0;
  display: flex; /* 使用 flex 布局 */
  flex-direction: row; /* 水平排列图表 */
}

.g1, .g2 {
  /* margin-top: 100px; */
  width: 50%; /* 设置宽度为50% */
  height: 100%;
}

body {
  height: 100%;
  margin: 0;
  width: 100%;
}
</style>