<template>
<div class="mx-4 cursor-pointer h-full overflow-hidden no-scrollbar">
  <div class="border flex justify-center mt-4">
    <div class="relative inline-block h-16">
      <div class="absolute block -inset-x-24 -inset-y-8 bg-lying-knife bg-no-repeat bg-center scale-75 rotate-180 transition-transform duration-500"></div>
    </div>
    <div @click="isOpen = !isOpen" class="relative inline-block w-full h-16">
      <GlowText :content="props.a.name"></GlowText>
    </div>
    <div class="relative inline-block h-16">
      <div class="absolute block -inset-x-24 -inset-y-8 bg-lying-knife bg-no-repeat bg-center scale-75 rotate-180 transition-transform duration-500"></div>
    </div>
  </div>
  <Transition name="slide-fade">
    <div ref="achievementReference" v-if="isOpen" class="bg-transparent text-white overflow-hidden">
      <div class="grid grid-cols-2 border text-sm text-center overflow-hidden">
        <div class="col-span-2 p-2"><GlowText :content="props.a.description"></GlowText></div>
        <div class="col-span-2 border-b mb-1"></div>
        <div class="border-r h-5"><GlowText :content="'Tier: ' + props.a.tier"></GlowText></div>
        <div class="border-l h-5"><GlowText :content="'Difficulty: ' + props.a.difficulty"></GlowText></div>
        <div class="col-span-2 border-y h-5"><GlowText :content="'Experience: ' + achievementEXP"></GlowText></div>
        <div class="border col-span-2 min-h-[20px]"><GlowText :content="props.a.reward"></GlowText></div>
      </div>
    </div>
  </Transition>
</div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { calcExp } from '@/help/extraFunctions'
import GlowText from '@/components/GlowText.vue'
import { useChapterStore } from '@/store/chapter'

const chapterStore = useChapterStore()

const props = defineProps({
  a: {
    type: Object,
    default: () => ({})
  }
})

const isOpen = ref(true)

const achievementEXP = calcExp({
  level: chapterStore.currentPlayer.level,
  tier: props.a.tier,
  power: props.a.difficulty,
  type: 'achievement'
})

const achievementReference = ref()
const computedHeight = { height: 0 }

onMounted(() => {
  const height = window.getComputedStyle(achievementReference.value, null).getPropertyValue('height')
  computedHeight.height = `${height}px`
  isOpen.value = false
})
</script>

<style>
.slide-fade-enter-active {
  transition: all 0.5s ease-out;
}

.slide-fade-leave-active {
  transition: all 0.5s ease-in;
}

.slide-fade-enter-from,
.slide-fade-leave-to {
  height: 0;
  opacity: 0;
}

.slide-fade-enter-to,
.slide-fade-leave-from {
  height: 100px;
}
</style>
