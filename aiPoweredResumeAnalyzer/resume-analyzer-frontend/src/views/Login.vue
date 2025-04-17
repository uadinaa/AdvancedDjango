<template>
  <v-container class="d-flex justify-center align-center" style="height: 100vh;">
    <v-card class="pa-6" max-width="400">
      <v-card-title class="text-h5 text-center">Login</v-card-title>
      <v-card-text>
        <v-form @submit.prevent="login">
          <v-text-field
            v-model="email"
            label="Email"
            type="email"
            required
          />
          <v-text-field
            v-model="password"
            label="Password"
            type="password"
            required
          />
          <v-btn type="submit" color="primary" block class="mt-4">
            Login
          </v-btn>
        </v-form>

        <!-- Additional Options -->
        <div class="text-center mt-4">
          <v-btn text small color="primary" @click="$router.push('/forgot-password')">
            Forgot Password?
          </v-btn>
          <br />
          <v-btn text small color="secondary" @click="$router.push('/register')">
            Don’t have an account? Register
          </v-btn>
        </div>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script>
import axios from '@/axios'

export default {
  name: 'UserLogin',
  data() {
    return {
      email: '',
      password: ''
    }
  },
  methods: {
    async login() {
      try {
        const res = await axios.post('auth/login/', {
          email: this.email,
          password: this.password
        })
        localStorage.setItem('access', res.data.access)
        this.$router.push('/dashboard')
      } catch (err) {
        alert('Login failed. Please check your email and password.')
      }
    }
  }
}
</script>
