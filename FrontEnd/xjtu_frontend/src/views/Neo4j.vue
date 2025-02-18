<template>
  <div ref="neo4jGraph" class="graph-container"></div>
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
      edges: new vis.DataSet([])
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
      MATCH (n)-[r]->(m)
      RETURN n,r,m LIMIT 100
    `;
    session
      .run(query)
      .then((result) => {
        if (result.records.length === 0) {
          console.warn("No data returned from the query.");
          return;
        }
        console.log("Query result:", result); // 添加调试信息
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
            console.log("Added node:", { id: node1Id, label: node1.properties.name || node1Id }); // 添加调试信息
          }
          if (!this.nodes.get(node2Id)) {
            this.nodes.add({ id: node2Id, label: node2.properties.name || node2Id });
            console.log("Added node:", { id: node2Id, label: node2.properties.name || node2Id }); // 添加调试信息
          }

          // 添加边
          this.edges.add({
            from: node1Id,
            to: node2Id,
            label: relationship.properties.type || ''
          });
          console.log("Added edge:", { from: node1Id, to: node2Id, label: relationship.properties.type || '' }); // 添加调试信息
        });

        // 创建网络
        const container = this.$refs.neo4jGraph;
        const data = {
          nodes: this.nodes,
          edges: this.edges
        };
        const options = {};
        new vis.Network(container, data, options);
        console.log("Network created with data:", data); // 添加调试信息
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
.graph-container {
  height: 100vh;
  width: 100vw;
}
</style>