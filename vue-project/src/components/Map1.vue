<script setup>
import {ref,computed,onMounted,onUnmounted} from 'vue';
import * as echarts from 'echarts'
import 'vue-echarts'
import axios from 'axios';
// const merchant_data=ref([])
const merchant_data=ref([
  {
    "name":"高需求",
    "children":[
      {
        "name":"北京",
        "value":[116.4074, 39.9042]
      },
      {
        "name":"上海",
        "value":[121.4737, 31.2304]
      },
      {
        "name":"广州",
        "value":[113.2644, 23.1291]
      },
      {
        "name":"深圳",
        "value":[114.0579, 22.5431]
      }
    ]
  },
  {
    "name":"中需求",
    "children":[
      {
        "name":"杭州",
        "value":[120.1535, 30.2876]
      },
      {
        "name":"成都",
        "value":[104.0627, 30.6501]
      },
      {
        "name":"武汉",
        "value":[114.3055, 30.5928]
      },
      {
        "name":"西安",
        "value":[108.9526, 34.2647]
      },
      {
        "name":"南京",
        "value":[118.7674, 32.0416]
      }
    ]
  },
  {
    "name":"低需求",
    "children":[
      {
        "name":"青岛",
        "value":[120.3351, 36.0648]
      },
      {
        "name":"天津",
        "value":[117.4219, 39.1344]
      },
      {
        "name":"厦门",
        "value":[118.1986, 24.4646]
      }
    ]
  }
]
)

//获取地图数据
const mapDataPath = '/static/map/china.json'
// const getMapData = async () => {
//     const response = await axios.get('/api/getMapData');
//     merchant_data.value = response.data;
// }
// onMounted(getMapData)
//图表配置项
const option = ref({})
//加载地图数据
const loadMapData = async()=>{
    try{
        //使用fetch 加载地图数据
        const response = await fetch(mapDataPath)
        const chinaMapData = await response.json()
        //注册地图数据
        echarts.registerMap('china',chinaMapData)

        //提取用户类型作为图例数据
        const legendData = merchant_data.value.map(group=> group.name)

        //将merchant_data转换成多个series数据
        const seriesData = merchant_data.value.map(group=>({
            name:group.name,
            type:'effectScatter',
            coordinateSystem:'geo',
            data:group.children.map(item=>({
                name:item.name,
                value:[...item.value,group.name]//将用户类型作为值的一部分，封装用户等级与对应城市坐标
            })),
            symbolSize:10,
            label:{
                show:true,
                formatter:'{b}'
            },
            itemStyle:{
                color:function(params){
                    //根据用户的类型设置颜色
                    const userTypes = {
                        '高需求':'#ffde93',
                        '中需求':'#87CEEB',
                        '低需求':'#FF6347'
                    }
                    return userTypes[params.value[2]]
                }
            }
        }))
        //设置ECharts配置项
        option.value = {
            title:{
                text:'招聘岗位分布',
                left:40,
                top:10
            },
            legend:{
                data:legendData,//图例数据
                selected:{
                    '高需求':true,
                    '中需求':true,
                    '低需求':true
                },
                top:'75%',
                left:'10%',
                orient:'vertical',//图例排列方向
                textStyle:{
                    color:'#4a5568'
                }
            },
            geo:{
                map:'china',
                roam:true,
                // zoom:1.5
                center:[104.114129,35.71514],
                itemStyle:{
                    areaColor: '#2E72BF',//地图区域颜色
                    borderColor:'#333',//边界线颜色
                    borderWidth:1//边界线宽度
                },
                emphasis:{
                    itemStyle:{
                        areaColor: '#ffde93',//地图区域颜色
                        borderColor:'#fff',//边界线颜色
                        borderWidth:1//边界线宽度
                    }
                }
            },
            series:seriesData
        }

    }catch(error){
        console.error('加载地图数据失败:',error)
    }
}
onMounted(loadMapData)
</script>

<template>
    <div class="com-container">
        <div class="com-chart">
            <e-charts :option="option" class="chart"></e-charts>
        </div>
    </div>
</template>

<style scoped lang="scss">

</style>