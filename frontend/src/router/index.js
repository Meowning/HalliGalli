import { createRouter, createWebHistory } from 'vue-router'
import Welcome from '../components/Welcome.vue'
import Lobby from '../components/Lobby.vue'
import GameRoom from '../components/Game/GameRoom.vue'

const routes = [
  {
    path: '/',
    name: 'Welcome',
    component: Welcome
  },
  {
    path: '/lobby',
    name: 'Lobby',
    component: Lobby
  },
  {
    path: '/game/:roomId',
    name: 'GameRoom',
    component: GameRoom,
    props: true
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
