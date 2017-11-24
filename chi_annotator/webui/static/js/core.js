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


