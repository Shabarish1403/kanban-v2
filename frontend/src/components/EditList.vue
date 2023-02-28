<template>
    <div>
        <b-modal 
            :id="`editList${list.id}`" 
            title="Edit List"
            @ok="handleOk">
            <b-form ref="form" @submit.stop.prevent="handleSubmit">
                <b-form-group
                    label="List Name"
                    label-for="name"
                    :invalid-feedback="invalidFeedback"
                    :state="nameState">
                    <b-form-input
                        id="name"
                        v-model="list.name"
                        :state="nameState"
                        trim>
                    </b-form-input>
                </b-form-group>
            </b-form>
        </b-modal>
    </div>
</template>

<script>
export default {
    name: 'EditList',
    props: ['lst'],
    data() {
        return {
            list: {
                name: ''
            },
            lNames: []
        }
    },
    mounted() {
        this.list = this.lst
        this.lNames = this.listNames
    },
    computed: {
        listNames() {
            return this.$store.getters.listNames
        },
        nameState() {
            return (this.list.name.length > 0 && !this.lNames.includes(this.list.name))
        },
        invalidFeedback() {
            if (this.list.name.length == 0) {
                return 'Name is required'
            }
            if (this.lNames.includes(this.list.name)) {
                return 'Name already exists'
            }
            return 'please enter something'
        },
        editList() {
            return this.$store.getters.editList
        }
    },
    methods: {
        handleOk(bvModalEvent) {
            bvModalEvent.preventDefault()
            this.handleSubmit()
        },
        handleSubmit() {
            if (!this.nameState) {
                return
            }
            this.editList(this.list)
            this.$router.go()
            this.$nextTick(() => {
                this.$bvModal.hide(`editList${this.list.id}`)
            })

        }
    }
}
</script>