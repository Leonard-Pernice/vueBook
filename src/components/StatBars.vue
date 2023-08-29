<template>
  <div class="fixed h-screen w-4 z-10 top-0 right-0 overflow-x-visible overflow-y-hidden bg-black" v-if="navigationStore.showResBars">
    <div class="flex align-middle justify-center flex-col h-full">
      <div
        class="flex self-center mx-0 h-auto"
        v-for="(stat, i) in chapterStore.currentStats"
        :key="i"
        v-show="navigationStore.bars[stat.name]"
      >
        <div class="progress flex my-1 float-left w-2 h-32 max-h-fit bg-black border-solid border-white border">
          <div
            class="w-full h-0 transition ease-in-out delay-500 bg-blue-500" role="progressbar" :aria-valuenow="stat.bar" aria-valuemin="0" :aria-valuemax="calcTotal(stat)"
            :style="{ height: (stat.bar/calcTotal(stat)*100).toFixed(0)+'%', background: getColor(stat) }"></div>
        </div>
      </div>
    </div>
  </div>

</template>

<script setup>
import { useNavigationStore } from '@/store/index'
import { useChapterStore } from '@/store/chapter'
const navigationStore = useNavigationStore()
const chapterStore = useChapterStore()

function calcTotal (stat) {
  return Math.floor(stat.base + stat.increased + Math.floor(parseFloat(stat.trained)))
}

function getColor (stat) {
  switch (stat.name) {
    case 'Vitality':
      return 'red'
    case 'Momentum':
      return 'green'
    case 'Charisma':
      return 'pink'
    case 'Spirit':
      return 'blue'
    default:
      return ''
  }
}

</script>
