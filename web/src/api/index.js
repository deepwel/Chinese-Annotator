import axios from 'axios'

const axiosInstance = axios.create({ baseURL: 'http://localhost:8000/api' })

const apis = {
  getProjectInfo() {
    return axiosInstance.get('/project_info/')
  },
  getAnnotationHistoryList() {
    return axiosInstance.get('/query_annotation_history/')
  },
  //NOTICE: 默认是test.json
  loadDataSet(filepath = 'tests/data/test_email_classify/email_classify_chi_nolabel.txt') {
    return axiosInstance.get('/load_local_dataset/', { params: { filepath } })
  },
  getUnlabeledAnnotationList(offset = 0, limit = 10) {
    return axiosInstance.get('/load_all_unlabeled/', { params: { offset, limit } })
  },
  exportDataSet() {
    return axiosInstance.get('/export_data/')
  },
  annotateText(text, label, uuid) {
    return axiosInstance.post('/annotate_single_unlabeled/', {
      text,
      uuid,
      label,
    })
  },
  getAnnotationHistory(offset = 0, limit = 10) {
    return axiosInstance.get('/query_annotation_history/', {
      params: {
        offset,
        limit,
      },
    })
  },
}

export default apis
