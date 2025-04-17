import { createRouter, createWebHistory } from 'vue-router'

// General views
import Login from '@/views/Login.vue'
import Register from '@/views/Register.vue'
import Dashboard from '@/views/Dashboard.vue'
import EmailVerify from '@/views/EmailVerify.vue'
import PasswordResetRequest from '@/views/PasswordResetRequest.vue'
import PasswordResetConfirm from '@/views/PasswordResetConfirm.vue'
import JobMatchResults from "@/components/Match/JobMatchResults.vue"
import Feedback from "@/components/Feedback/Feedback.vue"
// Admin views
import AdminDashboard from '@/views/AdminDashboard.vue'
import ResumeList from '@/components/Admin/ResumeList.vue'
import JobList from '@/views/job/JobList.vue'
import UserList from '@/components/Admin/UserList.vue'
import NotAuthorized from '@/views/NotAuthorized.vue'

// Job feature views
import JobCreate from '@/views/job/JobCreate.vue'
import JobDetail from '@/views/job/JobDetail.vue'
import JobEdit from '@/views/job/JobEdit.vue'

const routes = [
  { path: '/', name: 'Dashboard', component: Dashboard },
  { path: '/login', name: 'Login', component: Login },
  { path: '/register', name: 'Register', component: Register },
  { path: '/dashboard', name: 'Dashboard', component: Dashboard },
  { path: '/verify-email', name: 'EmailVerify', component: EmailVerify },
  { path: '/reset-password', name: 'PasswordResetRequest', component: PasswordResetRequest },
  { path: '/reset-confirm', name: 'PasswordResetConfirm', component: PasswordResetConfirm },
  { path: '/403', name: 'NotAuthorized', component: NotAuthorized },
  // Admin
  {
    path: '/admin',
    name: 'AdminDashboard',
    component: AdminDashboard,
    meta: { requiresAuth: true, roles: ['admin'] }
  },
  {
    path: '/admin/resumes-list',
    name: 'ResumeList',
    component: ResumeList,
    meta: { requiresAuth: true, roles: ['admin'] }
  },
  {
    path: '/admin/job-list',
    name: 'JobListAdmin',
    component: JobList,
    meta: { requiresAuth: true, roles: ['admin'] }
  },
  {
    path: '/admin/user-list',
    name: 'UserList',
    component: UserList,
    meta: { requiresAuth: true, roles: ['admin'] }
  },

  // Job CRUD
  {
    path: '/jobs',
    name: 'JobList',
    component: JobList
  },
  {
    path: '/jobs/create',
    name: 'JobCreate',
    component: JobCreate,
    meta: { requiresAuth: true, roles: ['admin', 'recruiter'] }
  },
  {
    path: '/jobs/:id',
    name: 'JobDetail',
    component: JobDetail,
    props: true
  },
  {
    path: '/jobs/:id/edit',
    name: 'JobEdit',
    component: JobEdit,
    meta: { requiresAuth: true, roles: ['admin', 'recruiter'] },
    props: true
  },

  { path: '/job-match-results', name: 'JobMatchResults', component: JobMatchResults, meta: { requiresAuth: true, roles: ['user'] } },
  { path: '/feedback', name: 'Feedback', component: Feedback, meta: { requiresAuth: true, roles: ['user'] } },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 🔐 Navigation guard
router.beforeEach((to, from, next) => {
  const access = localStorage.getItem('access')
  const userRole = localStorage.getItem('role')

  if (to.meta.requiresAuth) {
    if (!access) {
      return next('/login')
    }

    if (to.meta.roles && !to.meta.roles.includes(userRole)) {
      return next('/403')
}
  }

  next()
})

export default router
