import Mock from 'mockjs'

const data = Mock.mock({
  basic: {
    type: '文本分类',
    dataSet: 'iccpol-train'
  },
  'sentences|10': [{
    'id|+1': 0,
    'content': '@csentence(100,200)',
    'annotation_id': null,
    'machine_annotation_id|0-2': 1
  }],
  annotations: [{
    id: 0,
    name: '体育'
  }, {
    id: 1,
    name: '财经'
  }, {
    id: 2,
    name: '房产'
  }, {
    id: 3,
    name: '家居'
  }, {
    id: 4,
    name: '教育'
  }, {
    id: 5,
    name: '科技'
  }, {
    id: 6,
    name: '时尚'
  }, {
    id: 7,
    name: '时政'
  }, {
    id: 8,
    name: '游戏'
  }, {
    id: 9,
    name: '娱乐'
  }]
})

export default {
  data
}
