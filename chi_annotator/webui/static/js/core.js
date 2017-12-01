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
        axios.post('/load_local_dataset',{
          filepath:  this.file_path,
        })
        .then(function (response) {
          this.message = response.data.message
          console.log(response);
        })
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
        })
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
            headers: { 'content-type': 'multipart/form-data' }
        }
        axios.post('/upload_remote_file', formData, config)
        .then(function (response) {
          this.message = response.data.message
          console.log(response);
        })
        .catch(function (error) {
          console.log(error);
        });
    },
    tirggerFile : function (event) {
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
        })
        .catch(function (error) {
          console.log(error);
        });
    },
  }
})

