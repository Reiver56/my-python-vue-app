import { createRouter, createWebHistory } from 'vue-router'
import Playground from './pages/Playground.vue'
import PipelineEditor from './pages/PipelineEditor.vue'

export default createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'Playground',
      component: Playground
    },
    {
      path: '/pipeline',
      name: 'PipelineEditor',
      component: PipelineEditor
    }
  ]
})
