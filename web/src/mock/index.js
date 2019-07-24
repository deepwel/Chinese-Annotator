import Mock from 'mockjs'

const data = Mock.mock({
  basic: {
    type: '文本分类',
    dataSet: 'iccpol-train',
  },
  'data|10': [
    {
      'id|+1': 0,
      text: '@csentence(100,200)',
      'machine_annotation_id|0-2': 1,
    },
  ],
  count: 10,
})

export default data
