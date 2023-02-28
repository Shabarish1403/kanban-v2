<template>
  <div>  
    <b-card align="center">
      <b-dropdown :text="card.name">
        <b-dropdown-item v-b-modal="`editCard${card.id}`">
          Edit<EditCard :crd="card" hidden></EditCard>
        </b-dropdown-item>
        <b-dropdown-item @click="deleteCard(listIndex, cardIndex, card.id)">Delete</b-dropdown-item>
      </b-dropdown>
      <b-form-checkbox v-model="flag" switch class="text-left"></b-form-checkbox>
      <b-card-text>{{card.content}}</b-card-text>
      <template #footer>
        <h6 class="" v-bind:style="{color:updateColor(listIndex,cardIndex)}"><b-icon icon="stopwatch-fill"></b-icon> {{card.deadline}}</h6>
      </template>
    </b-card>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name: 'MyCard',
  props: ['card','listIndex','cardIndex'],
  data() {
    return {
      flag: false,
      cardToggle: {
        id: this.card.id,
        toggle: this.card.toggle,
      }
    }
  },
  mounted() {
    if (this.card.toggle == 1) {
      this.flag = true
    }
  },
  watch: {
    flag: function() {
      if (this.flag) {
        this.cardToggle.toggle = "1"
      }
      else {
        this.cardToggle.toggle = "0"
      }
      this.toggleCard(this.cardToggle)
    }
  },
  computed: {
    ...mapGetters(['toggleCard', 'deleteCard','updateColor'])
  },
  methods: {
  }
}
</script>

<style scoped>
</style>