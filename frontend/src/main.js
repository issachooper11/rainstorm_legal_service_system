import {createApp} from 'vue'
import App from './App.vue'

// 1. 引入路由
import router from './router'

// 2. 引入 Element Plus 及其样式
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

// 3. 引入 Element Plus 图标库（方便后续菜单和按钮用图标）
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
// 4. 引入 Element Plus 简体中文包
import zhCn from 'element-plus/es/locale/lang/zh-cn'
const app = createApp(App)

// 注册所有图标
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    app.component(key, component)
}

app.use(router)
app.use(ElementPlus, {
    locale: zhCn,
})
app.mount('#app')