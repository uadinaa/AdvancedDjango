<template>
  <v-container>
    <h2>Job Listings</h2>
    <v-btn v-if="canEdit" color="primary" class="mb-4" @click="$router.push('/jobs/create')">
      + New Job
    </v-btn>

    <v-data-table :headers="headers" :items="jobs" class="elevation-1">
      <!-- eslint-disable-next-line vue/valid-v-slot -->
      <template v-slot:item.actions="{ item }">
<!--      <template #item.actions="{ item }">-->
        <v-btn icon small color="blue" @click="editJob(item.id)" v-if="canEdit">
          <v-icon>mdi-pencil</v-icon>
        </v-btn>
        <v-btn icon small color="red" @click="deleteJob(item.id)" v-if="canEdit">
          <v-icon>mdi-delete</v-icon>
        </v-btn>
      </template>
    </v-data-table>
  </v-container>
</template>

<script>
import jobService from '@/services/jobService';
import auth from '@/services/auth';

export default {
  data() {
    return {
      jobs: [],
      headers: [
        { text: 'Title', value: 'title' },
        { text: 'Description', value: 'description' },
        { text: 'Actions', value: 'actions', sortable: false }
      ],
      canEdit: false
    };
  },
  async created() {
    try {
      const res = await jobService.getJobs();
      this.jobs = res.data;

      const user = auth.getUser();
      this.canEdit = user && (user.role === 'admin' || user.role === 'recruiter');
    } catch (err) {
      console.error('Error fetching jobs:', err);
    }
  },
  methods: {
    editJob(id) {
      this.$router.push(`/jobs/${id}/edit`);
    },
    async deleteJob(id) {
      if (confirm('Are you sure you want to delete this job?')) {
        try {
          await jobService.deleteJob(id);
          this.jobs = this.jobs.filter(job => job.id !== id);
        } catch (err) {
          console.error('Error deleting job:', err);
        }
      }
    }
  }
};
</script>
