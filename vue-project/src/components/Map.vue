<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import * as echarts from 'echarts';
import axios from 'axios';

const merchant_data = ref([]);
const chartInstance = ref(null);

// 获取数据（增强错误处理）
const fetchMapData = async () => {
  try {
    const { data } = await axios.get('/api/getMapData', {
      baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000',
      timeout: 8000
    });

    if (data.status !== 'success') throw new Error(data.message || 'API返回异常');

    merchant_data.value = data.data.map(item => ({
      name: item.region,
      value: [...item.coordinates, `${item.demand_level}需求`],
      itemStyle: {
        color: {
          '高': '#FF0000',
          '中': '#FFA500',
          '低': '#008000'
        }[item.demand_level]
      }
    }));

  } catch (error) {
    console.error('API请求失败:', error);
    // 保底测试数据
    merchant_data.value = [
      { name: "北京", value: [116.4, 39.9, "高需求"], itemStyle: { color: '#FF0000' } },
      { name: "上海", value: [121.47, 31.23, "中需求"], itemStyle: { color: '#FFA500' } }
    ];
  }
};

// 初始化地图
const initChart = async () => {
  const chartDom = document.getElementById('map-container');
  if (!chartDom) {
    console.error('地图容器未找到');
    return;
  }

  // 销毁旧实例
  chartInstance.value?.dispose();

  try {
    // 动态加载地图数据
    const mapData = await fetch('/static/map/china.json').then(res => {
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      return res.json();
    });
    echarts.registerMap('china', mapData);
  } catch (e) {
    console.warn('地图JSON加载失败:', e);
  }

  // 初始化图表
  chartInstance.value = echarts.init(chartDom);
  updateChart();
};

// 更新图表配置
const updateChart = () => {
  if (!chartInstance.value) return;

  chartInstance.value.setOption({
    title: {
      text: '招聘需求分布',
      left: 'center'
    },
    tooltip: {
      trigger: 'item',
      formatter: params => {
        return `${params.name}<br/>需求等级: ${params.value[2]}`;
      }
    },
    geo: {
      map: 'china',
      roam: true,
      emphasis: {
        itemStyle: {
          areaColor: '#FFD700'
        }
      },
      itemStyle: {
        areaColor: '#F0F8FF',
        borderColor: '#404a59'
      }
    },
    series: [{
      type: 'effectScatter',
      coordinateSystem: 'geo',
      data: merchant_data.value,
      symbolSize: val => val[2].includes('高') ? 16 : 12,
      rippleEffect: {
        brushType: 'stroke',
        scale: 4
      },
      label: {
        show: true,
        formatter: '{b}',
        position: 'right'
      },
      emphasis: {
        scale: true
      }
    }]
  }, true);
};

// 生命周期
onMounted(async () => {
  await fetchMapData();
  await initChart();
  window.addEventListener('resize', handleResize);
});

onUnmounted(() => {
  window.removeEventListener('resize', handleResize);
  chartInstance.value?.dispose();
});

const handleResize = () => {
  chartInstance.value?.resize();
};
</script>

<template>
  <div 
    id="map-container"
    style="width: 100%; height: 600px; background: #f8fafc;"
  ></div>
</template>

<style scoped>
#map-container {
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}
</style>