<script setup>
import { RouterLink, RouterView } from 'vue-router'

</script>

<template>
  <RouterView></RouterView>
</template>

<style scoped>

</style>

<!-- <script setup>

import { RouterLink, RouterView } from 'vue-router'
import {ref,computed} from 'vue';

const data = ref([
  { name: '商家1', value: 100 },
  { name: '商家2', value: 200 },
  { name: '商家3', value: 300 },
]);

const option = computed(() => ({
  title: {
    text: '商家数据统计',
    left: 'center',
  },
  xAxis: {
    type: 'category',
    data: data.value.map(item => item.name),
  },
  yAxis: {
    type: 'value',
  },
  series: [
    {
      name: '商家数据',
      type: 'line',
      data: data.value,
      emphasis: {
        itemStyle: {
          shadowBlur: 10,
          shadowOffsetX: 0,
          shadowColor: 'rgba(0, 0, 0, 0.5)',
        },
      },
    },
  ],
}));
</script>

<template>
  <div style="width: 700px; height: 500px;">
    <e-charts class="chart" :option="option"></e-charts>
  </div>
</template>

<style scoped>

</style>
 -->
