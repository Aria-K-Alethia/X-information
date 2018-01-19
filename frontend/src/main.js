// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import Vuex from 'vuex'
import ElementUI from 'element-ui'
import store from './vuex/store'
import 'element-ui/lib/theme-chalk/index.css'
import App from './App'
import router from './router'
import echarts from 'echarts'

Vue.use(ElementUI)
Vue.use(Vuex)

Vue.prototype.$echarts = echarts

/* eslint-disable no-new */
new Vue({
  el: '#app',
  store,
  router,
  template: '<App/>',
  components: { App }
})
