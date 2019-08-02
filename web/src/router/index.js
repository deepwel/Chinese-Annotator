import Router from 'vue-router'
import Home from '@/pages/Home.vue'
import WorkingSpace from '@/pages/WorkingSpace.vue'

const router = new Router({
  mode: 'history',
  base: '/',
  routes: [
    { path: '*', redirect: '/' },
    {
      path: '/',
      component: Home,
      children: [
        {
          path: '/working_space',
          component: WorkingSpace,
        },
      ],
    },
  ],
})

export default router
