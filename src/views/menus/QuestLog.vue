<template>
  <div class="relative mt-16 mx-auto md:mt-20 bg-gradient-radial from-gr-inner-blue to-gr-outer-blue text-white overflow-hidden no-scrollbar">
    <div class="flex justify-center mb-4">
      <div class="relative inline-block w-full h-16">
        <div class="absolute block -inset-x-14 -inset-y-8 bg-lying-s bg-repeat-x bg-center"></div>
      </div>
      <div class="relative inline-block w-full h-16">
        <div class="absolute block -inset-x-14 -inset-y-8 bg-big-swirl bg-no-repeat bg-center"></div>
      </div>
      <div class="relative inline-block w-full h-16">
        <div class="absolute block -inset-x-14 -inset-y-8 bg-lying-s bg-repeat-x bg-center"></div>
      </div>
    </div>
    <div class="" v-for="(quest, i) in chapterStore.current.quests" :key="i">
      <QuestTemplate :q="quest"></QuestTemplate>
    </div>
    <div class="mt-2 flex justify-center">
      <div class="relative inline-block w-full h-14">
        <div class="absolute block -inset-x-14 -inset-y-8 bg-lying-s bg-repeat-x bg-center"></div>
      </div>
      <div class="relative inline-block w-full h-14">
        <div class="absolute block -inset-x-14 -inset-y-8 bg-lying-x bg-no-repeat bg-center"></div>
      </div>
      <div class="relative inline-block w-full h-14">
        <div class="absolute block -inset-x-14 -inset-y-8 bg-lying-s bg-repeat-x bg-center"></div>
      </div>
    </div>
  </div>
</template>

<script setup>
import QuestTemplate from '@/components/QuestTemplate.vue'
import { useChapterStore } from '@/store/chapter'

const chapterStore = useChapterStore()

// const placeholder = {
//   q1: { show: false, name: 'Aspen Apocalypse!', desc: 'Some Info', tier: 1, diff: 1, exp: 50, rewTitle1: 'T1', rewTitle2: 'T2', rew1: 'Nada', rew2: 'Nada' },
//   q2: { show: false, name: 'Goblins! I be thy end!', desc: 'Some Info', tier: 1, diff: 1, exp: 50, rewTitle1: 'T1', rewTitle2: 'T2', rew1: 'Nada', rew2: 'Nada' },
//   q3: { show: false, name: 'Escort Deluxe!', desc: 'Some Info', tier: 1, diff: 1, exp: 50, rewTitle1: 'T1', rewTitle2: 'T2', rew1: 'Nada', rew2: 'Nada' },
//   q4: { show: false, name: 'Title', desc: 'Some Info', tier: 1, diff: 1, exp: 50, rewTitle1: 'T1', rewTitle2: 'T2', rew1: 'Nada', rew2: 'Nada' },
//   q5: { show: false, name: 'Title', desc: 'Some Info', tier: 1, diff: 1, exp: 50, rewTitle1: 'T1', rewTitle2: 'T2', rew1: 'Nada', rew2: 'Nada' },
//   q6: { show: false, name: 'Title', desc: 'Some Info', tier: 1, diff: 1, exp: 50, rewTitle1: 'T1', rewTitle2: 'T2', rew1: 'Nada', rew2: 'Nada' }
// }
</script>
