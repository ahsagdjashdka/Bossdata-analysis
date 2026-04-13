<script setup>
import TrendPage from './TrendPage.vue';
import MapPage from './MapPage.vue';
import RankPage from './RankPage.vue';
import Hotpage from './HotPage.vue';
</script>

<template>
  <div class="screen-container">
    <header class="screen-header">
      <span class="title">Boss直聘岗位分析系统</span>
    </header>
    <div class="screen-body">
      <section class="screen-left">
        <div class="chart-container top-chart">
          <TrendPage/>
        </div>
        <div class="chart-container bottom-chart">
          <RankPage/>
        </div>
      </section>
      <section class="screen-middle">
        <div class="chart-container top-chart">
          <MapPage/>
        </div>
        <div class="chart-container bottom-chart">
          <Hotpage/>
        </div>
      </section>
    </div>
  </div>
</template>

<style lang="less" scoped>
.screen-container {
  width: 200%;
  height: 100vh;
  padding: 0;
  margin: 0;
  background-color: #161522;
  color: #fff;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.screen-header {
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 20px;
  flex-shrink: 0;
  
  .title {
    font-size: 20px;
    font-weight: bold;
    white-space: nowrap;
  }
}

.screen-body {
  flex: 1;
  display: flex;
  gap: 10px;
  padding: 0 10px 10px;
  overflow: hidden;

  > section {
    display: flex;
    flex-direction: column;
    gap: 10px;
    height: 100%;
  }
  
  .screen-left {
    flex: 0 0 45%;
    min-width: 0;
  }
  
  .screen-middle {
    flex: 1;
    min-width: 0;
  }
  
  .chart-container {
    background: #1a1a2e;
    border-radius: 6px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.15);
    display: flex;
    flex-direction: column;
    overflow: hidden;
    
    &.top-chart {
      flex: 1 1 60%;
    }
    
    &.bottom-chart {
      flex: 1 1 40%;
    }
  }
}
</style>