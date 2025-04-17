// services/jobService.js
import axios from 'axios';

const API = '/api/jobs/';

export default {
  listJobs() {
    return axios.get(API);
  },
  getJob(id) {
    return axios.get(`${API}${id}/`);
  },
  createJob(data) {
    return axios.post(`${API}create/`, data);
  },
  updateJob(id, data) {
    return axios.put(`${API}${id}/update/`, data);
  },
  deleteJob(id) {
    return axios.delete(`${API}${id}/delete/`);
  }
};

