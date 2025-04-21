<template>
  <div class="sidebar">
    <div class="icon">
      <LineChartOutlined class="icon-svg" />
      <h1>算法可视化平台</h1>
    </div>
    <div class="container">
      <div class="new-chat":class="{ active: $route.name === 'Neo4j' }" @click="navigateTo('Neo4j')"> 
        <div class="el-icon-plus">
          <RadarChartOutlined class="neo4j-svg" />
          <div class="text">全局节点展示</div>
        </div>
      </div>
      <div class="new-chat":class="{ active: $route.name === 'groundTruth' }" @click="navigateTo('groundTruth')">
        <div class="el-icon-plus">
          <DotChartOutlined class="groundtruth-svg"/>
          <div class="text">GroundTruth</div>
        </div>
      </div>
      <div class="new-chat":class="{ active: $route.name === 'DeepSeek' }" @click="navigateTo('DeepSeek')">
        <div class="el-icon-plus">
          <SearchOutlined  class="deepseek-svg"/>
          <div class="text">DeepSeek</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { LineChartOutlined,RadarChartOutlined,SearchOutlined,DotChartOutlined} from '@ant-design/icons-vue';
import { useCssVar } from '@vueuse/core'
import { commentProps } from 'ant-design-vue/es/comment';
export default {
  name: "Sidebar",
  components: {
    LineChartOutlined,
    RadarChartOutlined,
    SearchOutlined,
    DotChartOutlined,
  },
  methods: {
    navigateTo(page) {
      this.$router.push({ name: page });
    },
  }
};
</script>

<style scoped>
.sidebar {
  width: 100%;
  height: 100%;
  background-color: #151a33;
  color: white;
}

.container {
  width: 100%;
  height: 95%;
  background-color: #1e213a	;
  align-items: center;
  flex-direction: column;

  display: flex;
  justify-content: flex-start;
}

.icon {
  display: flex;
  color: white;
  align-items: center;
  gap: 10px;
  font-size: 16px;
  /* 添加字体大小 */
  font-weight: 900;
}

.icon i {
  color: white;
  /* 确保图标颜色为白色 */
  display: flex;
  justify-content: flex-start;
}

.icon-svg {
  align-items: center;
  font-size: 25px;
  margin-bottom: 10px;
}

h1 {
  font-size: 20px;
  font-weight: 700;
}

.new-chat {
  width: 95%;
  height: 40px;
  align-items: center;
  gap: 10px;
  padding: 12px;
  background-color: #1e213a;
  border-radius: 6px;
  margin-bottom: 10px;
  transition: background-color 0.3s ease;
}


.new-chat:hover {
  background-color: #1e40af; /* 鼠标悬浮蓝色高亮 */
  cursor: pointer;
}
.new-chat.active {
  background-color: #1e40af;
}
.history-list {
  margin-top: 20px;
}
.el-icon-plus {
  display: flex;
  align-items: center;
}
.text {
  font-size: 15px;
  font-weight: 550;
  margin-left: 10px;
}
</style>