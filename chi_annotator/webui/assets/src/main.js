// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'

import VueRouter from 'vue-router'
import App from './App'

Vue.use(VueRouter)

Vue.config.productionTip = false

const app = new Vue({
	template : "<App/>",
	components : {App}
}).$mount('#app');

