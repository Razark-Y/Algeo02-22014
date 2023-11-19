import { createRouter, createWebHistory } from 'vue-router'
import Home from './View/HomeView.vue'
import ImageBased from './View/ImageBased.vue'
import CameraBased from './View/CameraBased.vue'
import WebScraper from './View/WebScraper.vue'
import About from './View/AboutView.vue'
import Docs from './View/DocView.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/ImageBased',
    name: 'Image',
    component: ImageBased
  },
  {
    path: '/CameraBased',
    name: 'Camera',
    component: CameraBased
  },
  {
    path: '/Scraper',
    name: 'Scraper',
    component: WebScraper
  },
  {
    path: '/About',
    name: 'About',
    component: About
  },
  {
    path: '/Docs',
    name: 'Docs',
    component: Docs
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
