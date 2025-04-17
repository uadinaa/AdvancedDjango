<template>
  <v-list>
    <v-list-item
      v-for="resume in resumes"
      :key="resume._id"
    >
      <v-list-item-title>{{ resume.user_id }}</v-list-item-title>
    </v-list-item>
  </v-list>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import axios from 'axios'

const resumes = ref([])

onMounted(async () => {
  const res = await axios.get('/api/resumes/', {
    headers: {
      Authorization: `Bearer ${localStorage.getItem('access')}`
    }
  })
  resumes.value = res.data
})
</script>
