import Vue from 'vue'
import VueRouter from 'vue-router'
import LoginView from '../views/LoginView.vue'
import DashBoard from '../views/DashBoard.vue'
import MySummary from '../views/MySummary.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'LoginView',
    component: LoginView
  },
  {
    path: '/dashboard',
    name: 'DashBoard',
    component: DashBoard,
    // props: true
  },
  {
    path: '/summary',
    name: 'MySummary',
    component: MySummary
  }
]

const router = new VueRouter({
  routes
})

export default router
