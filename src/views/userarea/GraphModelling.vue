<template>
  <div ref="p5Container"></div>
  <button @click="accountPage()" class="fixed inset-x-1/2 bottom-0 transform -translate-x-1/2 -translate-y-1/2 mb-4 button is-danger">Back to Account</button>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useAccountStore } from '@/store/account'
// import { onMounted, ref } from 'vue'
// import { p5 } from 'p5'

const router = useRouter()

// const p5Container = ref()

// const sketch = p => {
//   // Your sketch code here
//   p.setup = () => {
//     // Set up the canvas and other sketch properties
//     const canvas = p.createCanvas(400, 400)
//     canvas.parent('p5Container')
//     p.background(200)
//   }

//   p.draw = () => {
//     // Your draw code here
//     p.fill(0)
//     p.ellipse(p.mouseX, p.mouseY, 50, 50)
//   }
// }

// onMounted(() => {
//   // eslint-disable-next-line
//   const myP5 = new p5(sketch)
// })

// // onMounted(() => {
// //   new p5(sketch, p5Container)
// // })

// // const sketch = p => {
// //   p.setup = function () {
// //     p.createCanvas(400, 400)
// //     p.background(255, 0, 0)
// //   }
// //   p.draw = function () {
// //     p.background(255, 0, 0)
// //     p.fill(0, 255, 0)
// //     p.rect(p.width / 2, p.height / 2, 50, 50)
// //   }
// // }

// // const myp5 = new p5(sketch, p5Container)

const accountStore = useAccountStore()
function accountPage () {
  router.push(accountStore.isAuthenticated ? '/account' : '/login')
}
</script>
