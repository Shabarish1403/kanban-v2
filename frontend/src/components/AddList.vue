<template>
    <div>
        <b-modal 
            id="addList" 
            title="Add List"
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
    name: 'AddList',
    data() {
        return {
            list: {
                name: '',
            },
        }
    },
    computed: {
        userData() {
            return this.$store.state.userData
        },
        listNames() {
            return this.$store.getters.listNames
        },
        addList() {
            return this.$store.getters.addList
        },
        nameState() {
            return (this.list.name.length > 0 && !this.listNames.includes(this.list.name))
        },
        invalidFeedback() {
            if (this.list.name.length == 0) {
                return 'Name is required'
            }
            else if (this.listNames.includes(this.list.name)) {
                return 'Name already exists'
            }
            return 'please enter something'
        },
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
            this.addList(this.list)
            this.$router.go()
            this.$nextTick(() => {
                this.$bvModal.hide('addList')
                this.list.name = ''
            })

        }
    }
}
</script>