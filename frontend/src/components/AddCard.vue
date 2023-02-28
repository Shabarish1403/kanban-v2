<template>
    <div>
        <b-modal 
            :id="`addCard${list.id}`" 
            title="Add Card"
            @ok="handleOk">
            <b-form ref="form" @submit.stop.prevent="handleSubmit">
                <!-- <b-form-group label-for="list-name">
                    <b-form-select id="list-name" v-model="listID" :options="getOptions"></b-form-select>
                </b-form-group> -->
                <b-form-group label-for="name" 
                    :invalid-feedback="nameInvalidFeedback"
                    :state="nameState">
                    <b-form-input
                        id="name"
                        v-model="card.name"
                        placeholder="Card Name"
                        :state="nameState"
                        trim>
                    </b-form-input>
                </b-form-group>
                <b-form-group label-for="content">
                    <b-form-textarea
                        id="content"
                        placeholder="Content"
                        rows="3"
                        max-rows="6"
                        v-model="card.content">
                    </b-form-textarea>
                </b-form-group>
                <b-form-group label-for="deadline" 
                    :invalid-feedback="dateInvalidFeedback"
                    :state="dateState">
                    <b-form-datepicker
                        id="deadline"
                        placeholder="Deadline"
                        v-model="card.deadline"
                        :state = "dateState"
                        >
                    </b-form-datepicker>
                </b-form-group>
            </b-form>
        </b-modal>
    </div>
</template>

<script>
export default {
    name: 'AddCard',
    props: ['list'],
    data() {
        return {
            listID: this.list.id,
            card: {
                name: '',
                content: '',
                deadline: '',
            },
        }
    },
    mounted() {
    },
    computed: {
        userData() {
            return this.$store.state.userData
        },
        getOptions() {
            return this.$store.getters.getOptions
        },
        cardNames() {
            return this.$store.getters.cardNames
        },
        addCard() {
            return this.$store.getters.addCard
        },
        nameState() {
            return (this.listID != null && this.card.name.length > 0 && !this.cardNames(this.listID).includes(this.card.name))
        },
        nameInvalidFeedback() {
            // console.log(this.cardNames(this.listID))
            // if (this.listID == null) {
            //     return 'Please select the list'
            // }
            if (this.card.name.length == 0) {
                return 'Name is required'
            }
            else if (this.cardNames(this.listID).includes(this.card.name)) {
                return 'Name already exists'
            }
            return 'Please enter something'
        },
        dateState() {
            const today = new Date()
            const deadline = new Date(this.card.deadline)
            return (deadline >= today)
        },
        dateInvalidFeedback() {
            const today = new Date()
            const deadline = new Date(this.card.deadline)
            if (deadline < today) {
                return 'Date must be greater than today'
            }
            return 'Please enter valid date'
        }
    },
    methods: {
        handleOk(bvModalEvent) {
            bvModalEvent.preventDefault()
            this.handleSubmit()
        },
        handleSubmit() {
            if (!this.nameState || !this.dateState) {
                return
            }
            this.addCard(this.listID, this.card)
            this.$router.go()
            this.$nextTick(() => {
                this.$bvModal.hide('addCard')
                // this.listID = null
                this.card.name = ''
                this.card.content = ''
                this.card.deadline = ''
            })
        },
    }
}
</script>