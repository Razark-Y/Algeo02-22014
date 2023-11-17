import { createRouter, createWebHistory } from 'vue-router'
import ImageBased from "./View/ImageBased.vue"
import CameraBased from './View/CameraBased.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: CameraBased
  },
  {
    path: '/ImageBased',
    name: 'Image',
    component: ImageBased
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
