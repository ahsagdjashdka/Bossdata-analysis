import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

//配置element-plus
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
//配置echarts
import Echarts from 'vue-echarts'
import * as echarts from 'echarts'

//导入全局css文件
import './assets/css/global.less'

//导入字体文件
import '@/assets/font/iconfont.css'

const app = createApp(App)

app.use(createPinia())
app.use(router)
//将element-plus加载到主文件中
app.use(ElementPlus)

//加载echarts
app.component('e-charts',Echarts)
app.config.globalProperties.$echarts = echarts

app.mount('#app')
