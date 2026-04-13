<script setup>
//准备工具
import {ref,computed,onMounted,onUnmounted,markRaw} from 'vue';
import * as echarts from 'echarts'
import 'vue-echarts'

//静态数据
const optionData = ref({
    "map": {
        "title": "地区薪资趋势",
        "base": 3000,
        "unit": "元",
        "data": [{
            "name": "上海",
            "data": ["15513","15465","17146","16438","23723","30065","24029","23207","19331","13670","4864","9020"]
        }, {
            "name": "北京",
            "data": ["8625","3380","14558","2179","17609","13241","29105","19189","15154","9425","14175","15714"]
        }, {
            "name": "深圳",
            "data": ["14394","18629","18364","25148","19548","15216","5247","18412","20379","3916","5637","16164"]
        }, {
            "name": "广州",
            "data": ["5760","7761","30724","16505","17541","27688","26904","29611","10531","28339","13408","26538"]
        }, {
            "name": "重庆",
            "data": ["20082","21556","24980","22267","21698","6012","30968","27335","15099","25197","2615","18699"]
        }]
    },
    "seller": {
        "title": "行业薪资趋势",
        "base": 3000,
        "unit": "元",
        "data": [{
            "name": "计算机软件",
            "data": ["13200","12000","15000","18000","20000","22000","25000","27000","30000","32000", "15000", "18000"]
        }, {
            "name": "计算机硬件",
            "data": [  "20000","11000","12000","13000","14000","15000","16000","17000","18000","19000", "20000", "21000"]
        }, {
            "name": "计算机服务",
            "data": ["7354","4092","8981","11341","7634","10715","5561","20000","10629","7830","9805","3867"]
        }, {
            "name": "互联网",
            "data": ["4719","7357","4460","8403","6282","1565","6472","8898","2925","541","7911","11846"]
        }, {
            "name": "企业服务",
            "data": ["7484","11645","10769","1103","1731","4222","9760","10864","4387","11065","5960","3841"]
        }]
    },
    "commodity": {
        "title": "学历薪资趋势",
        "base": 3000,
        "unit": "元",
        "data": [{
            "name": "学历不限",
            "data": ["4771","1334","1930","793","4193","2301","2263","2691","62","3923","4874","2948"]
        }, {
            "name": "大专",
            "data": ["4666","4652","2365","173","4426","4707","1786","4020","378","3146","2801","863"]
        }, {
            "name": "本科",
            "data": ["2698","3071","4259","2950","2686","1765","3015","1585","928","3020","3235","3446"]
        }, {
            "name": "硕士",
            "data": ["2026","4623","4384","4675","2829","3236","4530","1673","4040","4507","2986","4192"]
        }, {
            "name": "博士",
            "data": ["758","2366","3978","3020","2572","3620","4755","3539","2785","3756","1691", "391"]
        }]
    },
    "common": {
        "month": ["一月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月"]
    },
    "type": [{
        "key": "map",
        "text": "地区薪资趋势"
    }, {
        "key": "seller",
        "text": "行业薪资趋势"
    }, {
        "key": "commodity",
        "text": "学历薪资趋势"
    }]
})
//图表实例
const trendChart = ref(null)
let chartInstance = null
//初始化图表
const initChart = ()=>{
    //echarts图表初始化，并返回初始化对象
    chartInstance = markRaw(echarts.init(trendChart.value))
    const initOption = {
        tooltip:{
            trigger:'axis'
        },
        grid:{
            left:'3%',
            top:'20%',
            right:'4%',
            bottom:'10%',
            containLabel:true
        },
        legend:{
            left:30,
            top:'5%',
            icon:'square',
            textStyle:{
                color:'#4a5568'
            }
        },
        xAxis:{
            type:'category',
            boundarGap:false
        },
        yAxis:{
            type:'value',
            axisLine:{
                lineStyle:{
                    color:'#555'
                }
            }
        }
    }
    chartInstance.setOption(initOption)
}

//获得数据
const getData = ()=>{
    updateChart()
}

//处理数据
const updateChart = ()=>{
    //配置色值
    const colorPalette = [
    { line: '#5B8FF9', area: 'rgba(91, 143, 249, 0.2)' }, // 蓝色系
    { line: '#5AD8A6', area: 'rgba(90, 216, 166, 0.2)' }, // 绿色系
    { line: '#F6BD16', area: 'rgba(246, 189, 22, 0.2)' }, // 黄色系
    { line: '#E8684A', area: 'rgba(232, 104, 74, 0.2)' }, // 红色系
    { line: '#6DC8EC', area: 'rgba(109, 200, 236, 0.2)' }  // 浅蓝系
  ];
    //x轴数据
    const timeArr = optionData.value.common.month
    //y轴数据
    const valueArr = optionData.value[choiceType.value].data
    //对y轴数据进一处理，获得series数据
    const seriesArr = valueArr.map((item,index) =>{
        return {
            name:item.name,
            type:'line',
            data:item.data,
            stack:choiceType.value,
            smooth:true,//曲线平滑
            areaStyle:{
                color: colorPalette[index].area, // 区域颜色
      opacity: 0.9 // 区域透明度
            }
        }
    })
    
    //绘制图列
    const legendArr = valueArr.map(item=>{
        return item.name
    })
    //配置图表
    const dataOption = {
        grid:{
            left:'1%',
            top:'15%',
            right:'1%',
            bottom:'10%',
            containLabel:true
        },
        xAxis:{
            data:timeArr,
            axisLabel:{
                interval:0,//显示所有标签
                color:'#4a5568',
            }
        },
        yAxis:{
            axisLine:{
                lineStyle:{
                    color:'#4a5568'
                }
            }
        },
        legend:{
            data:legendArr
        },
        series:seriesArr
    }
    chartInstance.setOption(dataOption)
}

//页面元素加载时对图表初始化
onMounted(()=>{
    initChart()
    getData()
})

//显示数据类型
const showChoice = ref(false)//是否显示可选项
const choiceType = ref('map')//显示数据类型。
//查询选中的文本
const handleSelect = (currentType)=>{
    console.log(currentType)
    choiceType.value = currentType //将转递来的数据给显示数据类型赋值
    updateChart()
    showChoice.value = false
}
//显示标题
const showTitle = computed(()=>{
    return optionData.value[choiceType.value].title
})
//过滤类型
const selectType = computed(()=>{
    return optionData.value.type.filter(itme=>{
        return itme.key !== choiceType.value
    })
})
</script>
<template>
  <div class="com-container">
    <div class="title">
      <div class="tab-switch">
        <div 
          v-for="item in optionData.type" 
          :key="item.key"
          class="tab-item"
          :class="{ active: choiceType === item.key }"
          @click="handleSelect(item.key)"
        >
          {{ item.text }}
        </div>
      </div>
    </div>
    <div class="com-chart" ref="trendChart"></div>
  </div>
</template>

<style scoped lang="scss">
.tab-switch {
  display: flex;
  gap: 10px;
  margin-left: 20px;
  
  .tab-item {
    padding: 4px 12px;
    border-radius: 4px;
    cursor: pointer;
    background: #5B8FF9;
    transition: all 0.3s;
    
    &.active {
      background: #3f6bc3;
      color: white;
    }
    
    &:hover:not(.active) {
      background: #5B8FF9;
    }
  }
}
</style> 