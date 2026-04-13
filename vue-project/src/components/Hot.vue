<script setup>
import {ref,computed,onMounted,onUnmounted} from 'vue';
import * as echarts from 'echarts';
import 'vue-echarts';
import { formatter } from 'element-plus';

//准备静态数据
const hotData = ref([
  {
    "name": "JAVA",
    "children": [
      {
        "name": "开发工程师",
        "value": 633,
        "children": [
          {
            "name": "本科",
            "value": 538
          },
          {
            "name": "大专",
            "value": 56
          },
          {
            "name": "硕士",
            "value": 39
          }
        ]
      },
      {
        "name": "研发工程师",
        "value": 175,
        "children": [
          {
            "name": "本科",
            "value": 149
          },
          {
            "name": "大专",
            "value": 16
          },
          {
            "name": "硕士",
            "value": 10
          }
        ]
      },
      {
        "name": "架构师",
        "value": 129,
        "children": [
          {
            "name": "本科",
            "value": 94
          },
          {
            "name": "大专",
            "value": 24
          },
          {
            "name": "硕士",
            "value": 11
          }
        ]
      },
      {
        "name": "项目经理",
        "value": 14,
        "children": [
          {
            "name": "本科",
            "value": 8
          },
          {
            "name": "大专",
            "value": 5
          },
          {
            "name": "硕士",
            "value": 1
          }
        ]
      },
      {
        "name": "软件工程师",
        "value": 288,
        "children": [
          {
            "name": "本科",
            "value": 267
          },
          {
            "name": "大专",
            "value": 12
          },
          {
            "name": "硕士",
            "value": 9
          }
        ]
      },
      {
        "name": "其他",
        "value": 209,
        "children": [
          {
            "name": "本科",
            "value": 168
          },
          {
            "name": "大专",
            "value": 26
          },
          {
            "name": "大专",
            "value": 15
          }
        ]
      }
    ]
  },
  {
    "name": "Python",
    "children": [
      {
        "name": "AI工程师",
        "value": 480,
        "children": [
          {
            "name": "本科",
            "value": 443
          },
          {
            "name": "大专",
            "value": 12
          },
          {
            "name": "硕士",
            "value": 25
          }
        ]
      },
      {
        "name": "爬虫工程师",
        "value": 78,
        "children": [
          {
            "name": "本科",
            "value": 66
          },
          {
            "name": "大专",
            "value": 10
          },
          {
            "name": "硕士",
            "value": 2
          }
        ]
      },
      {
        "name": "工程师",
        "value": 534,
        "children": [
          {
            "name": "本科",
            "value": 464
          },
          {
            "name": "大专",
            "value": 50
          },
          {
            "name": "硕士",
            "value": 20
          }
        ]
      },
      {
        "name": "软件工程师",
        "value": 384,
        "children": [
          {
            "name": "本科",
            "value": 300
          },
          {
            "name": "大专",
            "value": 74
          },
          {
            "name": "硕士",
            "value": 10
          }
        ]
      },
      {
        "name": "讲师",
        "value": 38,
        "children": [
          {
            "name": "本科",
            "value": 10
          },
          {
            "name": "硕士",
            "value": 28
          }
        ]
      },
      {
        "name": "其他",
        "value": 211,
        "children": [
          {
            "name": "本科",
            "value": 190
          },
          {
            "name": "大专",
            "value": 10
          },
          {
            "name": "硕士",
            "value": 11
          }
        ]
      }
    ]
  },
  {
    "name": "人工智能",
    "children": [
      {
        "name": "算法工程师",
        "value": 430,
        "children": [
          {
            "name": "本科",
            "value": 291
          },
          {
            "name": "大专",
            "value": 100
          },
          {
            "name": "硕士",
            "value": 39
          }
        ]
      },
      {
        "name": "训练师",
        "value": 284,
        "children": [
          {
            "name": "本科",
            "value": 184
          },
          {
            "name": "大专",
            "value": 60
          },
          {
            "name": "硕士",
            "value": 40
          }
        ]
      },
      {
        "name": "产品经理",
        "value": 94,
        "children": [
          {
            "name": "本科",
            "value": 60
          },
          {
            "name": "大专",
            "value": 32
          },
          {
            "name": "硕士",
            "value": 2
          }
        ]
      },
      {
        "name": "测试工程师",
        "value": 339,
        "children": [
          {
            "name": "本科",
            "value": 239
          },
          {
            "name": "大专",
            "value": 90
          },
          {
            "name": "硕士",
            "value": 10
          }
        ]
      },
      {
        "name": "其他",
        "value": 127,
        "children": [
          {
            "name": "本科",
            "value": 111
          },
          {
            "name": "大专",
            "value": 10
          },
          {
            "name": "硕士",
            "value": 6
          }
        ]
      }
    ]
  }
]
)

const option = ref({})

//数据切换
let currentIndex = ref(0)

const loadHotData = ()=>{
    //获得一级数据
    const currentCategory= hotData.value[currentIndex.value]
    //获得二级数据
    const currentCategoryChidren = currentCategory.children
    //获得三级数据
     const seriesData = currentCategoryChidren.map(child =>({
        name:child.name,
        value:child.value,
        children:child.children
    }))

  
    // const womenWear = (hotData.value[currentIndex.value].children)

    // const womenWearChildren = womenWear.map(child =>({
    //     name:child.name,
    //     value:child.value
    // }))

    option.value = {
        title:{
            text:'热门岗位占比',
            left:40,
            top:10
        },
        legend:{
            top:'15%',
            icon:'circle',
            textStyle:{
                color:'#4a5568'
            }
        },
        tooltip:{
            show:true,
            formatter : arg =>{
                const thirdCategory = arg.data.children
                //计算第三级分类的总和
                let total = 0
                thirdCategory.forEach(item=>{
                    total += item.value
                })
                //计算三级分类的百分比
                let retStr = ''
                thirdCategory.forEach(item=>{
                    retStr += `
                    ${item.name}:${parseInt(item.value/total * 100) + '%'}
                    </br>
                    `
                })
                return retStr
            }
        },
        series:[
            {
                type:'pie',
                data:seriesData,
                radius:'60%',
                center:['50%','60%'],
                label:{
                    show:false
                },
                emphasis:{
                    label:{
                        show:true
                    },
                    labelLine:{
                        show:false
                    }
                }
            }
        ]
    }
}
onMounted(loadHotData)



//切换数据
//向左切换
const toLeft = ()=>{
    currentIndex.value--
    if(currentIndex.value<0){
        currentIndex.value = hotData.value.length - 1
    }
    loadHotData()
}
//向右切换
const toRight = ()=>{
    currentIndex.value++
    if(currentIndex.value==hotData.value.length){
        currentIndex.value = 0
    }
    loadHotData()
}

//右下角标题
const catName = computed(()=>{
    if(!hotData.value){
        return ''
    }else{
        return hotData.value[currentIndex.value].name
    }
})


</script>

<template>
    <div class="com-container">
        <div class="com-chart">
            <e-charts class="chart" :option="option"></e-charts>
            <span class="iconfont arr-left" @click="toLeft">&#xe6ef;</span>
            <span class="iconfont arr-right" @click="toRight">&#xe6ed;</span>
            <span class="cat-name">{{catName}}</span>
        </div>
    </div>
</template>
<style scoped lang="scss">
.com-container{
    position: relative;
    width: 100%;
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
}
.com-chart{
    width: 100%;
    height: 100%;
    z-index: 1;
}
.arr-left, .arr-right{
    position: absolute;
    top: 50%;
    transform: translateY(-50%);
    cursor: pointer;
    z-index: 2;
}
.arr-left{
    left:5%;
}
.arr-right{
    right:5%;
}
.cat-name{
    position: absolute;
    right: 30px;
    bottom: 10px;
}
</style>