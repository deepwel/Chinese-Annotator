/**
 * Created by Littlepeer on 2017/11/11.
 */
var app = new Vue({
  el: '#app',
  data: {
    message: 'Hello Vue!'
  }

})

var example2 = new Vue({
  el: '#example-2',
  data: {
    name: 'Vue.js',
    counter: 1
  },
  // define methods under the `methods` object
  methods: {
    greet: function (event) {
      // Make a request for a user with a given ID
      axios.get('localhost:5000/')
        .then(function (response) {
          console.log(response);
        })
        .catch(function (error) {
          console.log(error);
        });
    }
  }
})



axios.defaults.baseURL = 'http://localhost:5000';
// axios.interceptors.request.use(
//   config =>{
//     config.data = JSON.stringify(config.data)
//     config.headers = {
//       'Content-Type':'application/json'
//     }
//     return config;
//   }
// );

var load_local_data = new Vue({
  el: '#load_local_data',
  data: {
    message: "fill the local data file path",
    file_path: '',
  },
  // define methods under the `methods` object
  methods: {
    load_local_data_post: function (event) {
      // Make a request for a user with a given ID
      axios.post('/load_local_dataset', {
          filepath: this.file_path,
        })
        .then(function (response) {
          this.message = response.data.message
          console.log(response);
        }.bind(this))
        .catch(function (error) {
          console.log(error);
        });
    },
    load_local_data_get: function (event) {
      // Make a request for a user with a given ID
      axios.get('/load_local_dataset?filepath=' + this.file_path)
        .then(function (response) {
          this.message = response.data.message
          console.log(response);
        }.bind(this))
        .catch(function (error) {
          console.log(error);
        });
    }
  }
})

var upload_remote_file = new Vue({
  el: '#upload_remote_file',
  data: {
    files: "",
    message: "select file to do upload",
  },
  // define methods under the `methods` object
  methods: {
    upload_remote_file: function (event) {
      // Make a request for a user with a given ID
      let formData = new FormData();
      formData.append('file', this.files[0])
      const config = {
        headers: {
          'content-type': 'multipart/form-data'
        }
      }
      axios.post('/upload_remote_file', formData, config)
        .then(function (response) {
          this.message = response.data.message
          console.log(response);
        }.bind(this))
        .catch(function (error) {
          console.log(error);
        });
    },
    tirggerFile: function (event) {
      this.files = event.target.files
    }
  }
})

var export_data = new Vue({
  el: '#export_data',
  data: {
    message: "export data",
  },
  // define methods under the `methods` object
  methods: {
    export_data: function (event) {
      // Make a request for a user with a given ID
      axios.get('/export_data')
        .then(function (response) {
          this.message = response.data.message
          console.log(response);
        }.bind(this))
        .catch(function (error) {
          console.log(error);
        });
    },
  }
})

var load_and_annotation_data = new Vue({
  el: '#load_and_annotation_data',
  data: {
    auto_label: "label",
    annotation_text: "annotation text",
    message: "select file to do upload",
    incorrect_label: false,
    uuid:"",
    calss_list: [{
        name: "span"
      },
      {
        name: "nonspan"
      }
    ],
    annptaion_list: [{
        label: "span",
        text: "您好： 我是广州市实达贸易有限公司,现有剩余(广告.运输.服务.商品.) 等各种普通发票可以代开,只收2% 的税点 联 人: 张高伟 手 机:  13828415779",
      },
      {
        label: "nonspan",
        text: "那如果之前很多次用手啥的会有影响吗?那个叫不叫湿疹~~还是用过手的性质就跟女生跳鞍马导致那个啥啥破一样的性质~ 嗯",
      }
    ],
  },
  created: function () {
    this.load_single_unlabeled()
  },
  // define methods under the `methods` object
  methods: {
    load_single_unlabeled: function () {
      axios.get('/load_single_unlabeled')
        .then(function (response) {
          this.auto_label = "span"
          this.annotation_text = response.data.data.text
          this.uuid = response.data.data.uuid
          console.log(response);
        }.bind(this))
        .catch(function (error) {
          console.log(error);
        });
    },

    annotate_single_unlabeled: function () {
      // Make a request for a user with a given ID
      axios.post('/annotate_single_unlabeled', {
          label: this.auto_label,
          text: this.annotation_text
        })
        .then(function (response) {
          this.load_single_unlabeled()
          console.log(response);
        }.bind(this))
        .catch(function (error) {
          console.log(error);
        });
    },

    annotate_single_correct: function () {
      // Make a request for a user with a given ID
      axios.post('/annotate_single_unlabeled', {
          label: this.item,
          text: this.annotation_text
        })
        .then(function (response) {
          this.load_single_unlabeled()
          console.log(response);
        }.bind(this))
        .catch(function (error) {
          console.log(error);
        });
    },

    click_wrong_button: function () {
      this.incorrect_label = true
    },
  }
})

var annotation_history = new Vue({
  el: '#annotation_history',
  data: {
    annptaion_list: [{
        label: "span",
        text: "您好： 我是广州市实达贸易有限公司,现有剩余(广告.运输.服务.商品.) 等各种普通发票可以代开,只收2% 的税点 联 人: 张高伟 手 机:  13828415779",
      },
      {
        label: "nonspan",
        text: "那如果之前很多次用手啥的会有影响吗?那个叫不叫湿疹~~还是用过手的性质就跟女生跳鞍马导致那个啥啥破一样的性质~ 嗯",
      }
    ],
  },
})