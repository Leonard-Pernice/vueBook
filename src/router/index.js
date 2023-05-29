import pinia from '@/store/store.js'
import { useAccountStore } from '@/store/account'

import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const accountStore = useAccountStore(pinia)

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/character',
    name: 'Character',
    component: () => import('../views/menus/CharacterSheet.vue'),
    props: true,
    params: { back: true, lastPos: 0 }
  },
  {
    path: '/skills',
    name: 'Skills',
    component: () => import('../views/menus/SkillSheet.vue')
  },
  {
    path: '/quests',
    name: 'Quest Log',
    component: () => import('../views/menus/QuestLog.vue')
  },
  {
    path: '/achievements',
    name: 'Achievement Log',
    component: () => import('../views/menus/AchievementLog.vue')
  },
  {
    path: '/pacts',
    name: 'Pact Information',
    component: () => import('../views/menus/PactPage.vue')
  },
  {
    path: '/paragons',
    name: 'Paragon Information',
    component: () => import('../views/menus/ParagonPage.vue')
  },
  // {
  //   path: '/rightNav',
  //   name: 'right',
  //   component: () => import('../views/SidebarRight.vue')
  // },
  {
    path: '/signup',
    name: 'SignUp',
    component: () => import('../views/userarea/SignUp.vue')
  },
  {
    path: '/login',
    name: 'LogIn',
    component: () => import('../views/userarea/LogIn.vue')
  },
  {
    path: '/account',
    name: 'Account',
    component: () => import('../views/userarea/MyAccount.vue'),
    meta: {
      requireLogin: true
    }
  },
  {
    path: '/graphs',
    name: 'graphs',
    component: () => import('../views/userarea/GraphModelling.vue')
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
  scrollBehavior () {
    return { x: 0, y: 0 }
  }
})

router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requireLogin) && !accountStore.isAuthenticated) {
    next({ name: 'LogIn', query: { to: to.path } })
  } else {
    next()
  }
})

export default router
