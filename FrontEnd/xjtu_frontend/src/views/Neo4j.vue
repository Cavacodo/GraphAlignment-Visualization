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
        <div ref="neo4jGraph" class="graph-container"></div>
        <div ref="neo4jGraph2" class="graph-container"></div> <!-- 添加第二个图表容器 -->
        <!-- 添加对话框组件 -->
        <div ref="dialog">
          <el-dialog :visible.sync="dialogVisible" title="节点信息">
          <pre>{{ selectedNode }}</pre>
          </el-dialog>
        </div>
      </el-main>
    </el-container>
  </div>
</template>

<script>
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
      dialogVisible: false, // 对话框显示状态
      selectedNode: null // 选中的节点信息
    };
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
          }
        };
        const network = new vis.Network(container, data, options);

        // 监听 selectNode 事件
        network.on('selectNode', (params) => {
          if (params.nodes.length > 0) {
            const nodeId = params.nodes[0];
            const node = this.nodes.get(nodeId);
            this.selectedNode = node;
            this.dialogVisible = true;
            console.log('Selected Node:', node); // 添加调试信息
            console.log('Dialog Visible:', this.dialogVisible); // 添加调试信息
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
          nodes:{
            color:{
              background: '#8BC34A',
              border: '#333',
              highlight: {
                background: '#66BB6A', 
                border: '#2e7d32'
              }
            }
          },
          edges:{
            color:{
              color: '#000', // 红色
              highlight: '#000' // 红色
            }
          }
        };
        const network2 = new vis.Network(container2, data2, options2);

        // 监听 selectNode 事件
        network2.on('selectNode', (params) => {
          if (params.nodes.length > 0) {
            const nodeId = params.nodes[0];
            const node = this.nodes2.get(nodeId);
            this.selectedNode = node;
            this.dialogVisible = true;
            console.log('Selected Node:', node); // 添加调试信息
            console.log('Dialog Visible:', this.dialogVisible); // 添加调试信息
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

.graph-container {
  height: 100%; /* 调整图表容器的高度 */
  width: 50%; /* 调整图表容器的宽度 */
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

body {
  height: 100%;
  margin: 0;
  width: 100%;
}
</style>