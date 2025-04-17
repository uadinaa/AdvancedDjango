import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import vuetify from './plugins/vuetify' // if you created this file
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

const app = createApp(App)

const vuetifyInstance = createVuetify({
  components,
  directives,
})

app.use(router)
app.use(vuetifyInstance)
app.use(vuetify)
app.mount('#app')


