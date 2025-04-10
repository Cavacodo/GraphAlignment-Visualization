<template>
    <div class="sidebar">
      <div class="new-chat" @click="navigateTo('Neo4j')">
        <i class="el-icon-plus"></i>
        全局节点展示
      </div>
      <div class="new-chat" @click="navigateTo('groundTruth')">
        <i class="el-icon-plus"></i>
        GroundTruth
      </div>
      <div class="new-chat" @click="navigateTo('DeepSeek')">
        <i class="el-icon-plus"></i>
        DeepSeek
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: "Sidebar",
    methods: {
      navigateTo(page) {
        this.$router.push({ name: page });
      }
    }
  };
  </script>
  
  <style scoped>
  .sidebar {
    width: 100%;
    height: 100%;
    background-color: #202123;
    padding: 20px;
    color: white;
  }
  
  .new-chat {
    height: 50px;
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 12px;
    background-color: #343541;
    border-radius: 6px;
    cursor: pointer;
    transition: background-color 0.3s;
    margin-bottom: 10px
  }
  
  .new-chat:hover {
    background-color: #40414f;
  }
  
  .history-list {
    margin-top: 20px;
  }
  </style>