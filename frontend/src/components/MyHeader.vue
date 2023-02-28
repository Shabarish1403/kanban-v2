<template>
  <div>
    <b-navbar toggleable="lg" type="dark" variant="primary" fixed="top">
      <b-navbar-brand to="/dashboard"><p class="h3"><b> Welcome {{userData.name}}</b></p></b-navbar-brand>

      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>
      <b-collapse id="nav-collapse" is-nav>

      <!-- Right aligned nav items -->
      <b-navbar-nav class="ml-auto">
        <b-navbar-nav>
          <b-nav-item-dropdown text="Add" right>
            <b-dropdown-item v-b-modal.addList>List</b-dropdown-item><AddList hidden></AddList>
            <b-dropdown-item v-b-modal.addCard>Card</b-dropdown-item><AddCard hidden></AddCard>
          </b-nav-item-dropdown>
          <b-nav-item to="/dashboard">Dashboard</b-nav-item>
          <b-nav-item to="/summary">Summary</b-nav-item>
          <b-nav-item @click="exportData">Export</b-nav-item>
        </b-navbar-nav>

        <b-nav-item-dropdown right>
          <template #button-content>
            <em>My Account</em>
          </template>
          <b-dropdown-item href="#">Profile</b-dropdown-item>
          <b-dropdown-item @click="logout">Sign Out</b-dropdown-item>
        </b-nav-item-dropdown>
      </b-navbar-nav>
      </b-collapse>
    </b-navbar>
  </div>
</template>

<script>
import { excelParser } from "../excel-parser";

export default {
  name: 'MyHeader',
  computed: {
    userData() {
      return this.$store.state.userData
    }
  },
  methods: {
    logout() {
      this.$store.dispatch('logoutUser')
    },
    async export(userID, listID) {
      const req = await fetch(`http://127.0.0.1:5000/api/export/${userID}/${listID}`,{
        headers: {
          'Content-Type': 'application/json',
          'Authentication-Token':localStorage.getItem('token')
        }
      })
      const data = await req.json()
      return data
    },
    async exportData() {
      // fetch('http://127.0.0.1:5000/export')
      const data = await this.export(this.userData.id, null)
      excelParser().exportDataFromJSON(data, null, 'csv');
      // return alert('Export completed successfully')
    },
  }
}
</script>

<style scoped>
</style>