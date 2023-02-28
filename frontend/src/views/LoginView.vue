<template>
  <div class="" style="">
      <b-row class="content">
        <b-col class="text-center" style="padding-top:80px; padding-right:120px">
          <b-container class="">
            <b-icon icon="card-checklist" font-scale="20" animation="fade"></b-icon>
            <h1 class="" style="position:relative">Kanban App</h1>
          </b-container>
        </b-col>
        <div class="vertical"></div>
        <b-col style="padding-top:80px;padding-left:120px">
          <LogIn @logon="logon" v-if="show"></LogIn>
          <SignUp @logon="logon" v-else></SignUp>
        </b-col>
      </b-row>
  </div>
</template>

<script>
export default {
  name: 'LoginView',
  data() {
    return {
      show: true
    }
  },
  methods: {
    logon() {
      this.show = !this.show
    }
  }
}
</script>

<style scoped>
.content {
  max-width: 1200px;
  padding-top:50px;
  margin: auto;
}
.vertical {
      border-left: 1px solid rgb(225, 224, 224);
      height: 600px;
      position:relative;
      left: 0%;
    }
</style>
