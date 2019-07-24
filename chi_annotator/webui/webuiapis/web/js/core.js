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



axios.defaults.baseURL = 'http://127.0.0.1:8000/api';
// axios.interceptors.request.use(
//   config =>{
//     config.data = JSON.stringify(config.data)
//     config.headers = {
//       'Content-Type':'application/json'
//     }
//     return config;
//   }
// );



var project_info = new Vue({
  el: '#project_info',
  data: {
    message: "Click Test to see if can connect Backend REST, and got project info",
    project_info: '',
  },
  // define methods under the `methods` object
  methods: {
    get_project_info: function (event) {
      // Make a request for a user with a given ID
      axios.get('/project_info/')
        .then(function (response) {
          this.message = "REST Status: " + response.data.message
          this.project_info = "Project Info: " + response.data.data
          console.log(response);
        }.bind(this))
        .catch(function (error) {
          this.message = "Error Failed to Connect"
        });
    },
  }
})

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
      axios.post('/load_local_dataset/', {
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
      axios.get('/load_local_dataset/?filepath=' + this.file_path)
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
    message: "Select file to do upload",
  },
  // define methods under the `methods` object
  methods: {
    upload_remote_file: function (event) {
      // Make a request for a user with a given ID
      var formData = new FormData();
      formData.append('file', this.files[0])
      axios.post('/upload_remote_file/', formData)
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
      axios.get('/export_data/')
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
    uuid: "",
    class_list: [{
      name: "span"
    },
    {
      name: "nonspan"
    }
    ],
  },
  // created: function () {
  //   this.load_single_unlabeled()
  // },
  // define methods under the `methods` object
  methods: {
    load_single_unlabeled: function () {
      this.incorrect_label = false
      axios.get('/load_single_unlabeled/')
        .then(function (response) {
          this.auto_label = "span"
          this.annotation_text = JSON.parse(response.data.data)
          this.uuid = annotation_text.uuid
          console.log(response);
        }.bind(this))
        .catch(function (error) {
          console.log(error);
        });
    },

    annotate_single_unlabeled: function () {
      // Make a request for a user with a given ID
      var params = new URLSearchParams();
      params.append('label', this.auto_label);
      params.append('text', this.annotation_text);
      params.append('uuid', this.uuid);
      axios.post('/annotate_single_unlabeled/', params)
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
      var params = new URLSearchParams();
      params.append('label', this.item);
      params.append('text', this.annotation_text);
      params.append('uuid', this.uuid);
      axios.post('/annotate_single_unlabeled/', params)
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
    history_annotation_number:1,
    history_annotation_page:0,
    annotation_list: [],
  },
  methods: {
    query_annotation_history: function (event) {
      var params = new URLSearchParams();
      params.append('RecNum', this.history_annotation_number);
      params.append('page_number', this.history_annotation_page);
      axios.get('/query_annotation_history/',{
        params: {
          'RecNum': this.history_annotation_number,
          'page_number': this.history_annotation_page
          }
        })
        .then(function (response) {
          this.annotation_list = JSON.parse(response.data.data)
          this.message = response.data.message
          console.log(response);
        }.bind(this))
        .catch(function (error) {
          console.log(error);
        });
    },
  }
})
