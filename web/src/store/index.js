import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    menuBarInfo: {
      basic: null,
    },
    history: [],
    progress: {
      count: 0,
      done: 0,
    },
    annotations: [
      {
        id: 0,
        name: '体育',
      },
      {
        id: 1,
        name: '财经',
      },
      {
        id: 2,
        name: '房产',
      },
      {
        id: 3,
        name: '家居',
      },
      {
        id: 4,
        name: '教育',
      },
      {
        id: 5,
        name: '科技',
      },
      {
        id: 6,
        name: '时尚',
      },
      {
        id: 7,
        name: '时政',
      },
      {
        id: 8,
        name: '游戏',
      },
      {
        id: 9,
        name: '娱乐',
      },
    ],
    dataSource: {
      data: [],
      count: 0,
    },
  },
  mutations: {
    updateHistory(state, history) {
      state.history = (history || []).reverse()
    },
    updateDataSource(state, dataSource) {
      state.dataSource = dataSource
    },
    updateProgress(state, progress) {
      state.progress = progress
    },
  },
})
