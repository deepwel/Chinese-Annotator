import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    interfaceUrl: null
  },
  mutations: {
    updateInterFaceUrl (state, url) {
      state.interfaceUrl = url
    }
  }
})
