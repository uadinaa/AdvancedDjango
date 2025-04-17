<template>
  <v-list>
    <v-list-item
      v-for="job in jobs"
      :key="job.id"
    >
      <v-list-item-title>{{ job.title }}</v-list-item-title>
    </v-list-item>
  </v-list>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import axios from 'axios'

const jobs = ref([])

onMounted(async () => {
  const res = await axios.get('/api/jobs/', {
    headers: {
      Authorization: `Bearer ${localStorage.getItem('access')}`
    }
  })
  jobs.value = res.data
})
</script>
