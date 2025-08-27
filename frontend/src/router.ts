import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from './views/Dashboard.vue'
import Note from './views/Note.vue'

export default createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', name: 'dashboard', component: Dashboard },
    { path: '/note/:id?', name: 'note', component: Note },
    { path: '/:pathMatch(.*)*', name: 'not-found', component: { template: '<div>404</div>' } }
  ],
})
