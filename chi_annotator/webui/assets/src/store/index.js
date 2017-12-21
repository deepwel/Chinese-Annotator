import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    menuBarInfo: {
      basic: null,
      progress: null
    }
  },
  mutations: {
    updateBasic (state, basic) {
      state.menuBarInfo.basic = basic
    },
    updateProgress (state, progress) {
      state.menuBarInfo.progress = progress
    }
  }
})
