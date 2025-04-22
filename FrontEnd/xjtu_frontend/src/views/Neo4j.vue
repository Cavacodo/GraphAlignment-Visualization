<template>
  <div class="main-container">
    <div class="display-layout">
      <el-aside width="200px">
        <SideBar />
      </el-aside>
      <div class="card-container">
        <el-card class="card">
          <div class="flex items-center space-x-4 p-4 bg-gray-50 rounded-lg">
            <!-- 类型选择器 -->
            <a-select v-model:value="selectedType" placeholder='选择类型' style="width: 120px"
              class="cascade!rounded-button">
              <a-select-option v-for="type in types" :key="type" :value="type">
                {{ type }}
              </a-select-option>
            </a-select>
            <!-- 算法选择器 -->
            <a-select v-model:value="selectedAlgorithm" placeholder="选择算法" style="width: 120px"
              class="cascade !rounded-button" @change="handleAlgorithmChange">
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
                  <div class="space-y-3" style="display: flex; flex-direction: column;">
                    <div v-for="alg in args" key="alg.key">
                    </div>
                </a-card>
              </template>
            </a-dropdown>
            <Button class="cascade" @click="handleClick">提交</Button>
          </div>
        </el-card>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { DownOutlined } from '@ant-design/icons-vue';
import SideBar from '../components/SideBar.vue';
import { Button } from 'ant-design-vue';
import { type } from 'os';
const selectedType = ref(null);
const selectedAlgorithm = ref(null);
const selectedKValue = ref(null);
const nodeId = ref('');
const types = ['网络1', '网络2'];
const algorithms = ['IsoRank', 'REGAL', 'DeepLink', 'BigAlign', 'FINAL', 'GAlign', 'GTCAlign'];
const kValues = [1, 2, 3, 4, 5];
const params = ref({
  maxIterations: null,
  learningRate: null,
  threshold: null
});
const dropdownVisible = ref(false);
const handleDropdownVisibleChange = (visible) => {
  dropdownVisible.value = visible;
};
const args = {
  'IsoRank': [
    { label: 'maxIteration', type: 'number', value: null, placeholder: 'maxIteration' },
    { label: 'alpha', type: 'float', value: null, placeholder: 'alpha' },
    { label: 'tol', type: 'float', value: null, placeholder: 'tol' },
    { label: 'K', type: 'number', value: null, placeholder: 'K' },
  ],
  'REGAL': [
    { label: 'attrvals', type: 'number', value: null, placeholder: 'attrvals' },
    { label: 'dimensions', type: 'numver', value: null, placeholder: 'dimensions' },
    { label: 'max_layer', type: 'number', value: null, placeholder: 'max_layer' },
    { label: 'K', type: 'number', value: null, placeholder: 'K' },
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
    { label: 'maxIteration', type: 'number', value: null, placeholder: 'maxIteration' },
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
}
//TODO 提交按钮
const handleClick = async () => {
  dropdownVisible.value = false;
};
</script>

<style scoped>
.main-container {
  height: 100vh;
  width: 100vw;
  background-color: #dedee0;
  margin: 0;
  padding: 0;
}

.display-layout {
  display: flex;
  height: 100%;
  width: 100%;
}

.card-container {
  padding: 10px;
  height: 100%;
  width: 100%;
  display: flex;
  align-items: center;
}

.card {
  width: 100%;
  height: 100%;
}


.trigger-input {
  width: 300px;
  cursor: pointer;
}

.custom-dropdown {
  padding: 10px;
  background: white;
  box-shadow: 0 0 6px rgba(0, 0, 0, 0.1);
  border-radius: 6px;
  width: 300px;
}

.input-group {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}

.label {
  width: 50px;
  text-align: right;
}

.flex-1 {
  margin: 2px;
  width: 100%;
}

.cascade {
  margin-left: 5px;
  margin-right: 5px;
}

:deep(.ant-select-selector) {
  border-radius: 6px !important;
}

:deep(.ant-input-number) {
  width: 100%;
}

:deep(.params-card .ant-card-body) {
  padding: 16px;
}
</style>
