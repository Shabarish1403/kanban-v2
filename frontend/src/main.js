import '@babel/polyfill'
import 'mutationobserver-shim'
import Vue from 'vue'
import './plugins/bootstrap-vue'
import App from './App.vue'
import router from './router'
import store from './store'
import './registerServiceWorker'
import MyHeader from '@/components/MyHeader.vue'
import MyList from '@/components/MyList.vue'
import MyCard from '@/components/MyCard.vue'
import NoLists from '@/components/NoLists.vue'
import AddList from '@/components/AddList.vue'
import EditList from '@/components/EditList.vue'
import AddCard from '@/components/AddCard.vue'
import EditCard from '@/components/EditCard.vue'
import LogIn from '@/components/LogIn.vue'
import SignUp from '@/components/SignUp.vue'


Vue.component('MyHeader',MyHeader)
Vue.component('MyList',MyList)
Vue.component('MyCard',MyCard)
Vue.component('NoLists',NoLists)
Vue.component('AddList',AddList)
Vue.component('EditList',EditList)
Vue.component('AddCard',AddCard)
Vue.component('EditCard',EditCard)
Vue.component('LogIn',LogIn)
Vue.component('SignUp',SignUp)


Vue.config.productionTip = false

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
