<template>
  <div>
    <MyHeader style="padding-top:80px"></MyHeader>
    <div v-if="this.userData.lists.length===0">
      <NoLists align=center></NoLists>
    </div>
    <div v-else class="card-columns m-4">
      <MyList v-for="(list, index) in userData.lists" 
        :key=list.id 
        :listIndex = index
        :list="list" 
        :cards="userData.lists[index].cards"
        style="padding-left:5px;padding-right:5px;padding-bottom:30px">
      </MyList>
    </div>
  </div>
</template>

<script>
export default {
  name: 'DashBoard',
  data() {
    return {
      show: false,
    }
  },
  computed: {
    userData() {
      return this.$store.state.userData
    }
  },
  async mounted() {
    await this.$store.dispatch('fetchData')
  },
}
</script>

<style scoped>
@media (min-width: 576px) {
  .card-columns {
    column-count: 2;
  }
}

@media (min-width: 768px) {
  .card-columns {
    column-count: 3;
  }
}

@media (min-width: 992px) {
  .card-columns {
    column-count: 4;
  }
}

@media (min-width: 1200px) {
  .card-columns {
    column-count: 5;
  }
}
</style>