<script setup>
import {ref,computed,onMounted,onUnmounted} from 'vue';
import * as echarts from 'echarts'
import 'vue-echarts'

//静态数据
const rankData = ref([
	{
		"name": "互联网",
		"value": 230
	},
	{
		"name": "计算机软件",
		"value": 214
	},
	{
		"name": "计算机硬件",
		"value": 203
	},
	{
		"name": "计算机服务",
		"value": 310
	},
	{
		"name": "媒体",
		"value": 289
	},
	{
		"name": "金融",
		"value": 207
	},
	{
		"name": "新能源",
		"value": 189
	},
	{
		"name": "医疗健康",
		"value": 195
	},
	{
		"name": "游戏",
		"value": 160
	},
	{
		"name": "数据服务",
		"value": 140
	}
	,
	{
		"name": "教育",
		"value": 120
	},
	{
		"name": "电子商务",
		"value": 110
	},
	{
		"name": "区块链",
		"value": 100
	},
	{
		"name": "人工智能",
		"value": 90
	},
	{
		"name": "云计算",
		"value": 80
	}
]
)
//Echarts配置项
const option = ref({})

//数据排序
const sortRankData = ()=>{
    rankData.value.sort((a,b)=> b.value - a.value)
}
//加载数据
const loadRankData = ()=>{
    //对数据排序
    sortRankData()
    //获取柱状图的x轴数据，y轴数据
    const names = rankData.value.map(item => item.name)
    const values = rankData.value.map(item => item.value)

    //设置配置项
    option.value = {
        title:{
            text:'行业岗位需求排名',
            left:40,
            top:10,
            color:'#fff'
        },
        grid:{
            top:'20%',
            left:'5%',
            right:'5%',
            bottom:'5%',
            containLabel:true
        },
        tooltip:{
            show:true
        },
        xAxis:{
            type:'category',
            data:names,
            axisLabel:{
                rotate:45,//倾斜45度
                interval:0,//强制显示
                color:'#4a5568'
            },

        },
        yAxis:{
            type:'value',
            axisLine:{
                lineStyle:{
                    color:'#4a5568'
                }
            },
        },
        series:[
            {
                name:'排名',
                type:'bar',
                data:values,
                label:{
                    show:true,
                    position:'top'

                },
                itemStyle:{
                    barBorderRadius:[20,20,0,0],
                    color:arg=>{
                        let targetColorArr = null
                        if(arg.value > 300){
                            targetColorArr = ['#0BA82C','#4FF778']
                        }else if(arg.value > 200 && arg.value < 300){
                            targetColorArr = ['#2E72BF','#23E5E5']
                        }else{
                            targetColorArr = ['#5052EE','#AB6EE5']
                        }
                        return new echarts.graphic.LinearGradient(0,0,1,0,[
                            {
                                offset:0,color:targetColorArr[0]
                            },{
                                offset:1,color:targetColorArr[1]
                            }
                        ])
                    }
                }
            }
            
        ]
    }
}
onMounted(loadRankData)
</script>

<template>
    <div class="com-container">
        <div class="com-chart">
            <e-charts class="chart" :option="option"></e-charts>
        </div>
    </div>
</template>
<style scoped lang="scss">

</style>