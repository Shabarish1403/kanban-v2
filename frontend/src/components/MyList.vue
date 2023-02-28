<template>
  <div>  
    <b-card img-src="../assets/image.jpg" img-alt="Image" img-top align="center">

      <div class="card-img-overlay">

        <b-row>
          <b-col class="text-left">
            <b-link style="color:black;" v-b-modal="`editList${list.id}`">
              <b-icon icon="pencil-square" scale="1.8"></b-icon>
            </b-link> 
            <EditList :lst="list" hidden></EditList>
          </b-col>
          <b-col class="text-center">
            <b-link style="color:black" @click="exportList">
              <b-icon icon="cloud-arrow-down" scale="1.8"></b-icon>
            </b-link>
          </b-col>
          <b-col class="text-right">
            <b-link style="color:black" @click="deleteList(listIndex,list.id)">
              <b-icon icon="trash" scale="1.8"></b-icon>
            </b-link>
          </b-col>
        </b-row>

        <b-row class="text-center m-auto" style="padding-top:35px">
          <b-button class="btn-lg col-12 text-wrap" variant="outline-dark">{{list.name}}</b-button>
        </b-row>
      </div>

      <b-card-text>
        <MyCard v-for="(card,index) in cards" 
          :key="card.id" 
          :card="card"
          :listIndex="listIndex"
          :cardIndex="index"
          style="padding-bottom:20px">
        </MyCard>
        
      </b-card-text>
      
      <template #footer>
        <small class="text-muted">{{lastUpdate(listIndex)}}</small>
      </template>
      <b-link style="color:black;" v-b-modal="`addCard${list.id}`">
          <b-icon icon="plus-circle" scale="1.8"></b-icon>
        </b-link>
        <AddCard :list="list" hidden></AddCard>
    </b-card>
    <!-- <b-icon icon="plus-circle" v-b-modal="`addCard${list.id}`">Add card</b-icon> -->

  </div>
</template>

<script>
import { excelParser } from "../excel-parser";

export default {
  name: 'MyList',
  props: ['list', 'cards', 'listIndex'],
  computed: {
    userData() {
      return this.$store.state.userData
    },
    deleteList() {
      return this.$store.getters.deleteList
    },
    lastUpdate() {
      return this.$store.getters.lastUpdate
    }
  },
  methods: {
    async export(userID, listID) {
      const req = await fetch(`http://127.0.0.1:5000/api/export/${userID}/${listID}`,{
        headers: {
          'Authentication-Token' : localStorage.getItem('token')
        }
      })
      const data = await req.json()
      return data
    },
    async exportList() {
      const data = await this.export(this.userData.id, this.list.id)
      excelParser().exportDataFromJSON(data, null, 'csv');
      // return alert('Export completed successfully')
    },
  }
}
</script>

<style scoped>
</style>