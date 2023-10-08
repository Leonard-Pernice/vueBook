<template>
<div class="mx-4 cursor-pointer h-full overflow-hidden no-scrollbar">
  <div class="border flex justify-center mt-4">
    <div class="relative inline-block h-16">
      <div class="absolute block -inset-x-24 -inset-y-8 bg-lying-knife bg-no-repeat bg-center scale-75 rotate-180 transition-transform duration-500"></div>
    </div>
    <div @click="isOpen = !isOpen" class="relative inline-block w-full h-16">
      <GlowText :content="props.q.name"></GlowText>
    </div>
    <div class="relative inline-block h-16">
      <div class="absolute block -inset-x-24 -inset-y-8 bg-lying-knife bg-no-repeat bg-center scale-75 rotate-180 transition-transform duration-500"></div>
    </div>
  </div>
  <Transition name="slide-fade">
    <div ref="questReference" v-if="isOpen" class="bg-transparent text-white overflow-hidden">
      <div class="grid grid-cols-2 border text-sm text-center overflow-hidden">
        <div class="col-span-2 p-2"><GlowText :content="props.q.description"></GlowText></div>
        <div class="col-span-2 p-2 pt-6" v-if="props.q.optional_description != ''"><GlowText :content="props.q.optional_description"></GlowText></div>
        <div class="col-span-2 border-b mb-1"></div>
        <div class="border-r h-5"><GlowText :content="'Tier: ' + props.q.tier"></GlowText></div>
        <div class="border-l h-5"><GlowText :content="'Difficulty: ' + props.q.difficulty"></GlowText></div>
        <div class="col-span-2 border-y h-5"><GlowText :content="'Experience: ' + calcExpQuest()"></GlowText></div>
        <div class="col-span-2 border h-5"><GlowText :content="props.q.reward_title"></GlowText></div>
        <div class="col-span-2 border min-h-[20px]"><GlowText :content="props.q.reward"></GlowText></div>
        <div class="col-span-2 border min-h-[20px]" v-if="props.q.optional_reward != ''"><GlowText :content="props.q.optional_reward"></GlowText></div>
      </div>
    </div>
  </Transition>
</div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import GlowText from '@/components/GlowText.vue'
import { useChapterStore } from '@/store/chapter'
import { calcExp } from '@/help/extraFunctions'

const chapterStore = useChapterStore()

function calcExpQuest () {
  const msg = {
    level: chapterStore.currentPlayer.level,
    power: props.q.difficulty,
    tier: props.q.tier,
    typ: 'quest'
  }
  return calcExp(msg)
}

const props = defineProps({
  q: {
    type: Object,
    default: () => ({})
  }
})

const isOpen = ref(true)

const questReference = ref()
const computedHeight = { height: 0 }

onMounted(() => {
  const height = window.getComputedStyle(questReference.value, null).getPropertyValue('height')
  computedHeight.height = `${height}px`
  isOpen.value = false
})

// const placeholder = {
//   q1: { show: false, name: 'Aspen Apocalypse!', desc: 'Some Info', tier: 1, diff: 1, exp: 50, rewTitle1: 'T1', rewTitle2: 'T2', rew1: 'Nada', rew2: 'Nada' },
//   q2: { show: false, name: 'Goblins! I be thy end!', desc: 'Some Info', tier: 1, diff: 1, exp: 50, rewTitle1: 'T1', rewTitle2: 'T2', rew1: 'Nada', rew2: 'Nada' },
//   q3: { show: false, name: 'Escort Deluxe!', desc: 'Some Info', tier: 1, diff: 1, exp: 50, rewTitle1: 'T1', rewTitle2: 'T2', rew1: 'Nada', rew2: 'Nada' },
//   q4: { show: false, name: 'Title', desc: 'Some Info', tier: 1, diff: 1, exp: 50, rewTitle1: 'T1', rewTitle2: 'T2', rew1: 'Nada', rew2: 'Nada' },
//   q5: { show: false, name: 'Title', desc: 'Some Info', tier: 1, diff: 1, exp: 50, rewTitle1: 'T1', rewTitle2: 'T2', rew1: 'Nada', rew2: 'Nada' },
//   q6: { show: false, name: 'Title', desc: 'Some Info', tier: 1, diff: 1, exp: 50, rewTitle1: 'T1', rewTitle2: 'T2', rew1: 'Nada', rew2: 'Nada' }
// }

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
