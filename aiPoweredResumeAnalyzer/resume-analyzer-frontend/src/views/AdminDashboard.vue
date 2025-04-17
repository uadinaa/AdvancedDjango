<template>
  <v-container>
    <v-row>
      <v-col cols="12" md="4">
        <v-card>
          <v-card-title>Users</v-card-title>
          <v-card-text>
            <UserList />
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" md="4">
        <v-card>
          <v-card-title>Jobs</v-card-title>
          <v-card-text>
            <JobList />
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" md="4">
        <v-card>
          <v-card-title>Resumes</v-card-title>
          <v-card-text>
            <ResumeList />
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import UserList from '@/components/Admin/UserList.vue'
import JobList from '@/components/Admin/JobList.vue'
import ResumeList from '@/components/Admin/ResumeList.vue'
</script>
