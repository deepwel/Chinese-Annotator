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
    name: '劳动纠纷'
  }, {
    id: 1,
    name: '刑事纠纷'
  }, {
    id: 2,
    name: '消费者权益保护'
  }]
})

export default {
  data
}
