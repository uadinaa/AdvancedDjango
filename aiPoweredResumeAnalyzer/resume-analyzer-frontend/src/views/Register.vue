<template>
  <v-container>
    <v-card>
      <v-card-title>Register</v-card-title>
      <v-card-text>
        <v-text-field v-model="username" label="Username" required />
        <v-text-field v-model="email" label="Email" type="email" required />
        <v-text-field v-model="password" label="Password" type="password" required />
        <v-select
          v-model="role"
          :items="roles"
          label="Select Role"
          required
        />
      </v-card-text>
      <v-card-actions>
        <v-btn color="primary" @click="register">Register</v-btn>
      </v-card-actions>
    </v-card>
  </v-container>
</template>

<script>
import axios from '@/axios'

export default {
  name: 'UserRegister',
  data() {
    return {
      username: '',
      email: '',
      password: '',
      role: '',
      roles: ['user', 'admin', 'recruiter'] // Customize based on your backend roles
    }
  },
  methods: {
    async register() {
      try {
        await axios.post('auth/register/', {
          username: this.username,
          email: this.email,
          password: this.password,
          role: this.role
        })
        alert('Check your email to verify your account.')
        this.$router.push('/login')
      } catch (err) {
        console.error(err.response?.data)
        alert('Registration failed: ' + JSON.stringify(err.response?.data))
      }
    }
  }
}
</script>
