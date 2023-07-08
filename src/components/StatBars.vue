<template>
  <div class="fixed h-screen w-4 z-10 top-0 right-0 overflow-x-visible overflow-y-hidden bg-black" v-if="navigationStore.showResBars">
    <div class="flex align-middle justify-center flex-col h-full">
      <div
        class="flex self-center mx-0 h-auto"
        v-for="(bar, i) in navigationStore.bars"
        :key="i"
        v-show="bar.show"
      >
        <div class="progress flex my-1 float-left w-2 h-32 max-h-fit bg-black border-solid border-white border">
          <div
            class="w-full h-0 transition ease-in-out delay-500 bg-blue-500" role="progressbar" :id="bar.type" :aria-valuenow="bar.current" aria-valuemin="0" :aria-valuemax="bar.total"
            :style="{ height: (bar.current/bar.total*100).toFixed(0)+'%', background: bar.color }"></div>
        </div>
      </div>
    </div>
  </div>

</template>

<script setup>
import { useNavigationStore } from '@/store/index'
const navigationStore = useNavigationStore()
</script>
