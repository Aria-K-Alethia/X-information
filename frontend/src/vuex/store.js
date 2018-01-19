import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

const store = new Vuex.Store({
  state: {
    // state relating to login
    username: '',
    is_login: false,
    // state relating to debug
    dev: true
  },
  mutations: {
  }
})
export default store
