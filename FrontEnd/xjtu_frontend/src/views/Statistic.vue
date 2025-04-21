<template>
    <div class="main-container">
        <div class="display-layout">
            <!-- 左侧边栏 -->
            <el-aside width="200px">
                <Sidebar />
            </el-aside>
        </div>
    </div>
</template>

<script>
import Sidebar from '../components/SideBar.vue';
export default {
    components: {
        Sidebar // Register the Sidebar component
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
</style>