import router from '@/router'
import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    userData: {},
    loggedIn: false
  },
  getters: {
    getUserData: (state) => {
      return state.userData
    },
    listNames: state => {
      const listNames = []
      for (let list of state.userData.lists) {
        listNames.push(list.name)
      }
      return listNames
    },
    addList: (state) => (list) => {
      fetch(`http://127.0.0.1:5000/api/createlist/${state.userData.id}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authentication-Token':localStorage.getItem('token')
        },
        body: JSON.stringify(list)
      }).then(r => console.log(r.json()))
    },
    editList: () => (list) => {
      fetch(`http://127.0.0.1:5000/api/updatelist/${list.id}`,{
        method:'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authentication-Token':localStorage.getItem('token')
        },
        body: JSON.stringify(list)
      })
    },
    deleteList: (state) => (listIndex, listID) => {
      if (confirm('Are you sure you want to delete?')) {
        state.userData.lists.splice(listIndex,1)
        fetch(`http://127.0.0.1:5000/api/deletelist/${listID}`,{
          method:'DELETE',
          headers: {
            'Content-Type': 'application/json',
            'Authentication-Token':localStorage.getItem('token')
          },
        })
      }      
    },
    getOptions: state => {
      const options = [
        {value: null, text: 'Please select a list'},
      ]
      for (let list of state.userData.lists) {
        const temp = {value: list.id, text: list.name}
        options.push(temp)
      }
      return options
    },
    cardNames: (state) => (listID) => {
      const cardNames = []
      const lists = state.userData.lists
      for (let list of lists) {
          if (list.id == listID) {
              for (let card of list.cards) {
                  cardNames.push(card.name)
              }
          }
      }
      return cardNames
    },
    addCard: () => (listID, card) => {
      fetch(`http://127.0.0.1:5000/api/createcard/${listID}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authentication-Token':localStorage.getItem('token')
        },
        body: JSON.stringify(card)
      })
    },
    editCard: () => (card) => {
      fetch(`http://127.0.0.1:5000/api/updatecard/${card.id}`,{
        method:'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authentication-Token':localStorage.getItem('token')
        },
        body: JSON.stringify(card)
      })
    },
    deleteCard: (state) => (listIndex, cardIndex, cardID) => {
      if (confirm('Are you sure you want to delete?')) {
        state.userData.lists[listIndex].cards.splice(cardIndex,1)
        fetch(`http://127.0.0.1:5000/api/deletecard/${cardID}`,{
          method:'DELETE',
          headers: {
            'Content-Type': 'application/json',
            'Authentication-Token':localStorage.getItem('token')
          },
        })
      }
    },
    toggleTrue: state => {
      const data = []
      for (let list of state.userData.lists) {
        let temp = 0
        for (let card of list.cards) {
          if (card.toggle == 1) {
            temp += 1
          }
        }
        data.push(temp)
      }
      return data
    },
    toggleFalse: state => {
      const data = []
      for (let list of state.userData.lists) {
        let temp = 0
        for (let card of list.cards) {
          if (card.toggle == 0) {
            temp += 1
          }
        }
        data.push(temp)
      }
      return data
    },
    toggleCard: () => (card) => {
      fetch(`http://127.0.0.1:5000/api/togglecard/${card.id}`,{
        method:'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authentication-Token':localStorage.getItem('token')
        },
        body: JSON.stringify(card)
      })
    },
    lastUpdate: (state) => (listIndex) => {
      let lastUpdate = new Date(state.userData.lists[listIndex].update_date).getTime()
      let now = new Date().getTime()
      let time = parseInt((now-lastUpdate)/(1000*60))
      let units = 'mins'
      if (time > 60) {
        time = parseInt(time/60)
        units = 'hours'
        if (time > 24) {
          time = parseInt(time/24)
          units = 'days'
        }
      }
      if (time<=1) {
        units = units.replace("s","")
      }
      return `Last updated ${time} ${units} ago`
    },
    updateColor: (state) => (listIndex, cardIndex) => {
      const card = state.userData.lists[listIndex].cards[cardIndex]
      let color = ''
      if (card.complete_date == 'Not completed') {
        let dt = new Date(card.deadline).getTime()
        let td = new Date().getTime();
        let diff = parseInt((dt-td)/(1000*60*60))
        if (0<diff && diff<24) {
          color = 'orange';
        }
        if (diff <= 0 ) {
          color = 'red'
        }
      }
      else {
        let dt = new Date(card.deadline).getTime()
        let cd = new Date(card.complete_date).getTime()
        let diff = dt-cd
        if (diff <= 0) {
          color = 'red'
        }
        else {
          color = 'green'
        }
      }
      return color
    }
  },
  mutations: {
    login(state) {
      state.loggedIn = true
    },
    logout(state) {
      state.loggedIn = false
    },
    getData: (state, data) => {
      state.userData = data
    },
    deleteList: (state, listID) => {
      for (let i in state.userData.lists) {
        if (state.userData.lists[i].id == listID) {
          delete state.userData.lists[i]
        }
      }
    },
    deleteCard: (state, cardID) => {
      for (let i in state.userData.lists) {
        for (let j in state.userData.lists[i].cards) {
          if (state.userData.lists[i].cards[j].id == cardID) {
            delete state.userData.lists[i].cards[j]
          }
        }
      }
    }
  },
  actions: {
    async fetchData(context) {
      const users = await fetch(`http://127.0.0.1:5000/api/${localStorage.getItem('email')}`,{
        headers:{
          "Authentication-Token":localStorage.getItem('token')
        }})
      const data = await users.json()
      context.commit('getData',data)
    },
    async loginUser({commit}, payload) {
      const login = await fetch('http://127.0.0.1:5000/login?include_auth_token',{
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
      })
      if (!login.ok) {
        alert('Incorrect email or password')
      }
      const data = await login.json()
      localStorage.setItem('email',payload.email)
      localStorage.setItem('token',data.response.user.authentication_token)
      commit('login')
      router.push('/dashboard')
    },
    logoutUser({commit}) {
      localStorage.clear()
      commit('logout')
      router.push('/')
    }
  },
  modules: {
  }
})
