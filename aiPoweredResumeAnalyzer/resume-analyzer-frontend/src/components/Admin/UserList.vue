<template>
  <v-list>
    <v-list-item
      v-for="user in users"
      :key="user.id"
    >
      <v-list-item-title>{{ user.username }} ({{ user.role }})</v-list-item-title>
    </v-list-item>
  </v-list>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import axios from 'axios'

const users = ref([])

onMounted(async () => {
  const res = await axios.get('/api/users/', {
    headers: {
      Authorization: `Bearer ${localStorage.getItem('access')}`
    }
  })
  users.value = res.data
})
</script>
