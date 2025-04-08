<script>
import Sidebar from "../components/Sidebar.vue"; // 引入 Sidebar 组件
import { reactive, ref } from 'vue'
import neo4j from "neo4j-driver";
import * as echarts from 'echarts';

let chart = null;
let chart2 = null;

export default {
  name: "Neo4jGraph",
  components: {
    Sidebar // 注册 Sidebar 组件
  },
  data() {
    return {
      nodes: [],
      edges: [],
      nodes2: [], // 添加第二个图表的节点数据集
      edges2: [],  // 添加第二个图表的边数据集
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
      const valueStr = Array.isArray(value) ? value.join('-') : value.toString();
      this.fetchData(valueStr, '网络1', this.nodes, this.edges, this.$refs.neo4jGraph);
    },
    handleChange2(value) {
      const valueStr = Array.isArray(value) ? value.join('-') : value.toString();
      this.fetchData(valueStr, '网络2', this.nodes2, this.edges2, this.$refs.neo4jGraph2);
    },
    fetchData(value, type, nodes, edges, container) {
      // 清空现有数据
      nodes.length = 0;
      edges.length = 0;

      // 连接到 Neo4j 数据库
      const driver = neo4j.driver(
        "bolt://localhost:7687",
        neo4j.auth.basic("neo4j", "neo4jpassword")
      );

      const session = driver.session();

      // 解析选中的范围，获取最小和最大 ID
      const [minId, maxId] = value.split('-').map(Number);
      console.log(minId, maxId);
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
          
          // 遍历查询结果并填充数据
          result.records.forEach((record) => {
            const node1 = record.get('n');
            const node2 = record.get('m');
            const relationship = record.get('r');
            const node1Id = node1.properties.id.toNumber();
            const node2Id = node2.properties.id.toNumber();
      

            // 根据 ID 过滤节点
            if (node1Id >= minId && node1Id <= maxId) {
              if (!nodes.find(n => n.id === node1Id)) {
                nodes.push({ id: node1Id, name: node1.properties.name || node1Id });
              }
            }
            if (node2Id >= minId && node2Id <= maxId) {
              if (!nodes.find(n => n.id === node2Id)) {
                nodes.push({ id: node2Id, name: node2.properties.name || node2Id });
              }
            }

            // 添加边
            if (nodes.find(n => n.id === node1Id) && nodes.find(n => n.id === node2Id)) {
              edges.push({
                source: node1Id,
                target: node2Id,
                label: relationship.properties.type || ''
              });
            }
          });

          // 创建图表数据
          const data = {
            nodes: nodes,
            links: edges
          };

          // 设置图表选项
          const option = {
            series: [{
              type: 'graph',
              layout: 'force',
              data: data.nodes.map(node => ({ ...node, x: null, y: null })),
              links: data.links,
              categories: [],
              roam: true,
              label: {
                show: true
              },
              force: {
                repulsion: 100
              },
              lineStyle: {
                opacity: 0.9,
                width: 2,
                curveness: 0
              },
              itemStyle: { // 添加 itemStyle 配置
                color: container === this.$refs.neo4jGraph ? 'blue' : 'red' // 设置不同图表的节点颜色
              }
            }]
          };

          // 创建图表
          // const chart = echarts.init(container);
          if(container === this.$refs.neo4jGraph) chart.setOption(option);
          else if(container === this.$refs.neo4jGraph2) chart2.setOption(option);
          else console.log("Error:", error);

          // 监听节点选择事件
          chart.on('click', (params) => {
            if (params.dataType === 'node') {
              this.dialogTableVisible = true;
              const nodeId = params.data.id;
              const node = nodes.find(n => n.id === nodeId);
              this.selectedNode = node;
              console.log('Selected Node:', node);

              // 获取邻居节点
              const neighbors = edges.filter(edge => edge.source === nodeId || edge.target === nodeId)
                .map(edge => edge.source === nodeId ? edge.target : edge.source)
                .map(id => nodes.find(n => n.id === id));

              // 填充 gridData
              this.gridData = [{
                id: node.properties.id,
                label: node.name,
                neighbor: neighbors.map(n => n.name).join(', '),
                align: '' // 可以根据需要填充
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
          if (!this.nodes.find(n => n.id === node1Id)) {
            this.nodes.push({ id: node1Id, name: node1.properties.name || node1Id });
          }
          if (!this.nodes.find(n => n.id === node2Id)) {
            this.nodes.push({ id: node2Id, name: node2.properties.name || node2Id });
          }

          // 添加边
          this.edges.push({
            source: node1Id,
            target: node2Id,
            label: relationship.properties.type || ''
          });
        });

        // 创建第一个网络
        const container = this.$refs.neo4jGraph;
        const data = {
          nodes: this.nodes,
          links: this.edges
        };
        const option = {
          series: [{
            type: 'graph',
            layout: 'force',
            data: data.nodes.map(node => ({ ...node, x: null, y: null })),
            links: data.links,
            categories: [],
            roam: true,
            label: {
              show: true
            },
            force: {
              repulsion: 100
            },
            lineStyle: {
              opacity: 0.9,
              width: 2,
              curveness: 0
            }
          }]
        };
        chart = echarts.init(container);
        chart.setOption(option);

        // 监听 selectNode 事件
        chart.on('click', (params) => {
          if (params.dataType === 'node') {
            this.dialogTableVisible = true; // 修改为 this.dialogTableVisible
            const nodeId = params.data.id;
            const node = this.nodes.find(n => n.id === nodeId);
            this.selectedNode = node;
            console.log('Selected Node:', node); // 添加调试信息

            // 获取邻居节点
            const neighbors = this.edges.filter(edge => edge.source === nodeId || edge.target === nodeId)
              .map(edge => edge.source === nodeId ? edge.target : edge.source)
              .map(id => this.nodes.find(n => n.id === id));

            // 填充 gridData 数组
            this.gridData = [{
              id: node.id,
              label: node.name,
              neighbor: neighbors.map(n => n.name).join(', '),
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
          if (!this.nodes2.find(n => n.id === node1Id)) {
            this.nodes2.push({ id: node1Id, name: node1.properties.name || node1Id });
          }
          if (!this.nodes2.find(n => n.id === node2Id)) {
            this.nodes2.push({ id: node2Id, name: node2.properties.name || node2Id });
          }

          // 添加边
          this.edges2.push({
            source: node1Id,
            target: node2Id,
            label: relationship.properties.type || ''
          });
        });

        // 创建第二个网络
        const container2 = this.$refs.neo4jGraph2;
        const data2 = {
          nodes: this.nodes2,
          links: this.edges2
        };
        const option2 = {
          series: [{
            type: 'graph',
            layout: 'force',
            data: data2.nodes.map(node => ({ ...node, x: null, y: null })),
            links: data2.links,
            categories: [],
            roam: true,
            label: {
              show: true
            },
            force: {
              repulsion: 100
            },
            lineStyle: {
              opacity: 0.9,
              width: 2,
              curveness: 0
            },
            itemStyle: { // 添加 itemStyle 配置
              color: 'red' // 设置 chart2 的节点颜色为红色
            }
          }]
        };
        chart2 = echarts.init(container2);
        chart2.setOption(option2);

        // 监听 selectNode 事件
        chart2.on('click', (params) => {
          if (params.dataType === 'node') {
            this.dialogTableVisible = true; // 修改为 this.dialogTableVisible
            const nodeId = params.data.id;
            const node = this.nodes2.find(n => n.id === nodeId);
            this.selectedNode = node;
            console.log('Selected Node:', node); // 添加调试信息

            // 获取邻居节点
            const neighbors = this.edges2.filter(edge => edge.source === nodeId || edge.target === nodeId)
              .map(edge => edge.source === nodeId ? edge.target : edge.source)
              .map(id => this.nodes2.find(n => n.id === id));

            // 填充 gridData 数组
            this.gridData = [{
              id: node.id,
              label: node.name,
              neighbor: neighbors.map(n => n.name).join(', '),
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