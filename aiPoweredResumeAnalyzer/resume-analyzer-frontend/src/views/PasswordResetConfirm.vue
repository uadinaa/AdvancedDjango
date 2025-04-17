<template>
  <v-container>
    <v-card>
      <v-card-title>Reset Your Password</v-card-title>
      <v-card-text>
        <v-text-field v-model="newPassword" label="New Password" type="password" />
      </v-card-text>
      <v-card-actions>
        <v-btn color="primary" @click="resetPassword">Reset</v-btn>
      </v-card-actions>
    </v-card>
  </v-container>
</template>

<script>
import axios from '@/axios'

export default {
  data() {
    return {
      newPassword: ''
    }
  },
  methods: {
    async resetPassword() {
      const token = this.$route.query.token
      try {
        await axios.post('auth/password-reset-confirm/', {
          token,
          password: this.newPassword
        })
        alert('Password has been reset. You can now log in.')
        this.$router.push('/login')
      } catch {
        alert('Reset failed.')
      }
    }
  }
}
</script>
