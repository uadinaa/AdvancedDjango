<template>
  <v-container>
    <h2>Edit Job</h2>
    <v-form ref="form" v-model="valid" lazy-validation>
      <v-text-field
        v-model="job.title"
        label="Job Title"
        :rules="[v => !!v || 'Title is required']"
        required
      />

      <v-textarea
        v-model="job.description"
        label="Job Description"
        :rules="[v => !!v || 'Description is required']"
        required
      />

      <v-btn color="primary" @click="updateJob" :disabled="!valid">Update Job</v-btn>
    </v-form>
  </v-container>
</template>

<script>
import jobService from '@/services/jobService';

export default {
  data() {
    return {
      valid: false,
      job: {
        title: '',
        description: ''
      }
    };
  },
  async created() {
    const jobId = this.$route.params.id;
    try {
      const res = await jobService.getJob(jobId);
      this.job = res.data;
    } catch (err) {
      console.error('Error loading job:', err);
    }
  },
  methods: {
    async updateJob() {
      if (this.$refs.form.validate()) {
        try {
          await jobService.updateJob(this.$route.params.id, this.job);
          this.$router.push('/jobs');
        } catch (err) {
          console.error(err);
        }
      }
    }
  }
};
</script>
