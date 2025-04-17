<template>
  <v-btn color="red" @click="logout">Logout</v-btn>
</template>

<script>
export default {
  methods: {
    logout() {
      localStorage.removeItem('access')
      localStorage.removeItem('refresh')
      this.$router.push('/login')
    }
  }
}
</script>
