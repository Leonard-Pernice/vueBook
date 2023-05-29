<template>
  <div class="align-middle justify-center flex items-center font-sans">
    <div class="mx-auto">
      <h1 class="text-4xl text-white mt-32 text-center field font-sans italic tracking-wide">Sign up</h1>
        <hr>
      <form @submit.prevent="submitForm">
        <div class="field">
          <label>Email Address</label>
          <div class="control">
            <input type="email" class="input" v-model="userdata.username" required>
          </div>
        </div>
        <label>Password</label>
        <div class="field has-addons">
          <div class="control is-expanded">
            <input v-if="showPassword" type="text" class="input" v-model="userdata.password">
            <input v-else type="password" class="input" v-model="userdata.password">
          </div>
          <div class="control">
            <button type="button" class="button is-right bg-gray-400" @click="toggleShowPassword">
              <div v-if="!showPassword" class="icon w-4 h-4">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 512" class="w-6 h-6">
                  <path :style="{fill: 'black'}" stroke-linecap="round" stroke-linejoin="round" d="M325.1 351.5L225.8 273.6c8.303 44.56 47.26 78.37 94.22 78.37C321.8 352 323.4 351.6 325.1 351.5zM320 400c-79.5 0-144-64.52-144-143.1c0-6.789 1.09-13.28 1.1-19.82L81.28 160.4c-17.77 23.75-33.27 50.04-45.81 78.59C33.56 243.4 31.1 251 31.1 256c0 4.977 1.563 12.6 3.469 17.03c54.25 123.4 161.6 206.1 284.5 206.1c45.46 0 88.77-11.49 128.1-32.14l-74.5-58.4C356.1 396.1 338.1 400 320 400zM630.8 469.1l-103.5-81.11c31.37-31.96 57.77-70.75 77.21-114.1c1.906-4.43 3.469-12.07 3.469-17.03c0-4.976-1.562-12.6-3.469-17.03c-54.25-123.4-161.6-206.1-284.5-206.1c-62.69 0-121.2 21.94-170.8 59.62L38.81 5.116C34.41 1.679 29.19 0 24.03 0C16.91 0 9.839 3.158 5.121 9.189c-8.187 10.44-6.37 25.53 4.068 33.7l591.1 463.1c10.5 8.203 25.57 6.333 33.69-4.073C643.1 492.4 641.2 477.3 630.8 469.1zM463.1 256c0 24.85-6.705 47.98-17.95 68.27l-38.55-30.23c5.24-11.68 8.495-24.42 8.495-38.08c0-52.1-43-96-95.1-96c-2.301 .0293-5.575 .4436-8.461 .7658C316.8 170 319.1 180.6 319.1 192c0 10.17-2.561 19.67-6.821 28.16L223.6 149.9c25.46-23.38 59.12-37.93 96.42-37.93C399.5 112 463.1 176.6 463.1 256z"></path>
                </svg>
              </div>
              <div v-else class="icon w-4 h-4">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" class="w-6 h-6">
                  <path :style="{fill: 'black'}" stroke-linecap="round" stroke-linejoin="round" d="M572.52 241.4C518.29 135.59 410.93 64 288 64S57.68 135.64 3.48 241.41a32.35 32.35 0 0 0 0 29.19C57.71 376.41 165.07 448 288 448s230.32-71.64 284.52-177.41a32.35 32.35 0 0 0 0-29.19zM288 400a144 144 0 1 1 144-144 143.93 143.93 0 0 1-144 144zm0-240a95.31 95.31 0 0 0-25.31 3.79 47.85 47.85 0 0 1-66.9 66.9A95.78 95.78 0 1 0 288 160z"></path>
                </svg>
              </div>
            </button>
          </div>
        </div>
        <div class="field">
          <label>Repeat password</label>
          <div class="control">
            <input type="password" class="input" v-model="userdata.password2">
            <div class="h-12 w-12 relative">
          </div>
          </div>
        </div>
        <div class="notification is-danger" v-if="userdata.errors.length">
          <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
        </div>
        <div class="field">
          <div class="">
            <button class="button is-success card-footer-item">Sign up</button>
          </div>
        </div>
        <hr>
        Or <RouterLink to="/login">click here</RouterLink> to log in!
      </form>
    </div>
  </div>
</template>

<script setup>
import axios from 'axios'
import { useRouter, useRoute } from 'vue-router'
import { computed, reactive } from 'vue'
import { useAccountStore } from '@/store/account'
import { useNavigationStore } from '@/store/index'
import { onMounted } from 'vue'

const router = useRouter()
const route = useRoute()
const accountStore = useAccountStore()
const navigationStore = useNavigationStore()

const userdata = reactive({
  username: '',
  password: '',
  password2: '',
  errors: []
})

const errors = computed(() => userdata.errors)

const page = reactive({
  password: true,
  hide: 'None',
  showPassword: false,
  isInvalid: false,
  hidden: 'hidden',
  shown: 'hidden',
  errorMessage: 'Password must be at least 8 characters long, and contain at least one uppercase letter, one lowercase letter, and one number.',
  passwordStrength: null
})

const showPassword = computed(() => page.showPassword)

onMounted(() => {
  navigationStore.showTopNav = false
})

function toggleShowPassword () {
  page.showPassword = !page.showPassword
  console.log(page.showPassword)
}

function checkPasswordStrength (password) {
  console.log(password)
  // const strengthRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$/
  // if (!password || !password.match(strengthRegex)) {
  //   return false
  // }
  return true
}

async function submitForm () {
  userdata.errors = []

  if (userdata.username === '') {
    userdata.errors.push('The username is missing.')
  }
  if (userdata.password !== userdata.password2) {
    userdata.errors.push('The passwords don\'t match.')
  }
  if (!checkPasswordStrength(userdata.password)) {
    userdata.errors.push('Password should be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, and one digit.')
  }
  if (!userdata.errors.length) {
    const formData = {
      email: userdata.username,
      username: userdata.username,
      password: userdata.password,
      re_password: userdata.password2
    }

    await axios
      .post('/api/v1/users/', formData)
      .then(response => {
        console.log(response)
        // toast({
        //   message: 'Account created, please log in!',
        //   type: 'is-success',
        //   dismissible: true,
        //   pauseOnHover: true,
        //   duration: 2000,
        //   position: 'bottom'
        // })
        axios
          .post('/api/v1/token/login/', {
            username: formData.username,
            password: formData.password
          })
          .then(response => {
            const token = response.data.auth_token
            accountStore.setToken(token)
            axios.defaults.headers.common.Authorization = 'Token ' + token
            localStorage.setItem('token', token)
            const toPath = route.query.to || '/'

            router.push(toPath)
          })
          .catch(error => {
            console.error(JSON.stringify(error))
            router.push('/login')
          })
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
  }
}

</script>
