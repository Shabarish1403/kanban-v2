<template>
    <div>
        <b-container style="max-width:300px;padding-top:80px" align="center">
            <h2>Welcome</h2>
            <b-form @submit="onSubmit" v-if="show">
                <b-form-group
                    label-for="email">
                    <b-form-input 
                        id="email" 
                        v-model="user.email" 
                        placeholder="Email" 
                        type="email"
                        required>
                    </b-form-input>
                </b-form-group>
                <b-form-group
                    label-for="username">
                    <b-form-input 
                        id="username" 
                        v-model="user.name" 
                        placeholder="Username" 
                        required>
                    </b-form-input>
                </b-form-group>
                <b-form-group
                    label-for="password">
                    <b-form-input 
                        id="password" 
                        v-model="user.password" 
                        placeholder="Enter Password" 
                        type="password"
                        trim
                        required>
                    </b-form-input>
                </b-form-group>
                <b-form-group
                    label-for="password2"
                    :state="state"
                    :invalid-feedback="invalidFeedback">
                    <b-form-input 
                        id="password2" 
                        v-model="user.password2" 
                        placeholder="ReEnter Password" 
                        type="password"
                        :state="state"
                        trim
                        required>
                    </b-form-input>
                </b-form-group>

                <b-button type="submit" variant="primary">Sign Up</b-button>
            </b-form>
            <small>Already have an account? <b-link @click="logon">Log In</b-link></small>
        </b-container>
    </div>
</template>

<script>
export default {
    name: 'LogIn',
    data() {
        return {
            show: true,
            user: {
                email: '',
                name: '',
                password: '',
                password2: ''
            }
        }
    },
    computed: {
        state() {
            return (this.user.password == this.user.password2)
        },
        invalidFeedback() {
            if (this.user.password != this.user.password2) {
                return 'Password not matches'
            }
            return 'retry'
        }
    },
    methods: {
        onSubmit(event) {
            event.preventDefault();
            // fetch call to login API
            fetch(`http://127.0.0.1:5000/api/adduser`, {
                method: 'POST',
                headers: {
                'Content-Type': 'application/json'
                },
                body: JSON.stringify(this.user)
                }).then(r => console.log(r.json()))
            this.$router.go()
        },
        logon() {
            this.$emit('logon')
        }
    }
}
</script>