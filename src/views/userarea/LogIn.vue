<template>
  <div class="h-screen w-screen align-middle justify-center flex items-center font-sans">
    <div class="mx-auto">
      <h1 class="text-4xl text-white mt-32 text-center field font-sans italic tracking-wide mb-4">Log in</h1>
        <hr>
      <form @submit.prevent="submitForm">
        <div class="mt-2">
          <label class="block text-white text-sm mb-2" for="email">Email Address</label>
          <input id="email" type="email" class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" v-model="userdata.username">
        </div>
        <div class="my-4">
          <label class="block text-white text-sm mb-2" for="password">Password</label>
          <input id="password" v-if="page.showPassword" type="text" class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" v-model="userdata.password">
          <input v-else type="password" class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" v-model="userdata.password">
          <button class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline" type="button" @click="toggleShowPassword"></button>
        </div>
        <div class="bg-red-500 text-white p-4 rounded-md" v-if="userdata.errors.length">
          <p v-for="error in userdata.errors" :key="error">{{ error }}</p>
        </div>
        <div class="card-footer">
          <button class="bg-green-400 hover:bg-green-500 text-white font-bold py-2 px-4 rounded-md w-full">Log in</button>
          <div class="flex-1">
          </div>
        </div>
        <hr>
        Or <RouterLink to="/signup">click here</RouterLink> to sign up!
      </form>
    </div>
  </div>
</template>

<script setup>
// import Vue from 'vue'
import axios from 'axios'
// import Cookies from 'js-cookie'
import { onMounted } from 'vue'
import { useAccountStore } from '@/store/account'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()
const accountStore = useAccountStore()

// const tokenCookies = function () {
//   return {
//     get: function (name) {
//       return Cookies.get(name)
//     },
//     set: function (name, value, attributes) {
//       Cookies.set(name, value, attributes)
//     },
//     remove: function (name, attributes) {
//       Cookies.remove(name, attributes)
//     }
//   }
// }

const userdata = {
  username: '',
  password: '',
  errors: []
}

const page = {
  password: true,
  hide: 'None',
  showPassword: false,
  isInvalid: false,
  hidden: 'hidden',
  shown: 'hidden',
  errorMessage: 'Password must be at least 8 characters long, and contain at least one uppercase letter, one lowercase letter, and one number.',
  passwordStrength: null
}

onMounted(() => {
  document.title = 'Log In | Book'
})

function toggleShowPassword () {
  page.showPassword = !page.showPassword
  console.log(page.showPassword)
}

async function submitForm () {
  console.log('Authentication: ' + accountStore.isAuthenticated)
  axios.defaults.headers.common.Authorization = ''
  localStorage.removeItem('token')

  userdata.errors = []

  if (userdata.username === '') {
    userdata.errors.push('The username is missing.')
  }
  if (userdata.password === '') {
    userdata.errors.push('Please enter your password.')
  }
  if (!userdata.errors.length) {
    const formData = {
      username: userdata.username,
      password: userdata.password
    }

    await axios
      .post('/api/v1/token/login/', formData)
      .then(response => {
        const token = response.data.auth_token
        accountStore.setToken(token)
        axios.defaults.headers.common.Authorization = 'Token ' + token
        localStorage.setItem('token', token)
        const toPath = route.query.to || '/'

        router.push(toPath)
      })
      .catch(error => {
        if (error.response) {
          for (const property in error.response.data) {
            userdata.errors.push(`${property}: ${error.response.data.property}`)
          }
        } else {
          userdata.errors.push('Something went wrong. Please try again.')
          console.log(JSON.stringify(error))
        }
      })

    console.log('Authentication: ' + accountStore.isAuthenticated)
  }
}

</script>
