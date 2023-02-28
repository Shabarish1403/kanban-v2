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
                    label-for="password">
                    <b-form-input 
                        id="password" 
                        v-model="user.password" 
                        placeholder="Password" 
                        type="password"
                        required>
                    </b-form-input>
                    <small style="padding-left:150px;"><b-link>Forgot Password?</b-link></small>
                </b-form-group>

                <b-button type="submit" variant="primary">Login</b-button>
            </b-form>
            <small>Don't have an account? <b-link @click="logon">Sign Up</b-link></small>
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
                password: ''
            }
        }
    },
    methods: {
        onSubmit(event) {
            event.preventDefault();
            // fetch call to login API
            this.$store.dispatch('loginUser',{email: this.user.email, password: this.user.password})
        },
        logon() {
            this.$emit('logon')
        }
    }
}
</script>