<template>
<div class="relative mt-16 mx-auto md:mt-20 bg-gradient-radial from-gr-inner-blue to-gr-outer-blue text-white overflow-x-hidden">
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
    <div class="" v-for="(achievement, i) in placeholder" :key="i">
        <Achievement :a="achievement"></Achievement>
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
import Achievement from '@/components/AchievementTemplate.vue'

const placeholder = {
  a1: { show: false, name: 'FIRST BLOOD!', desc: 'Some Info', tier: 1, diff: 1, exp: 50, rewTitle1: 'T1', rewTitle2: 'T2', rew1: 'Nada', rew2: 'Nada' },
  a2: { show: false, name: 'SPACE!! I NEED SPAAAACE!!!', desc: 'Some Info', tier: 1, diff: 1, exp: 50, rewTitle1: 'T1', rewTitle2: 'T2', rew1: 'Nada', rew2: 'Nada' },
  a3: { show: false, name: 'Made the world a better place', desc: 'Some Info', tier: 1, diff: 1, exp: 50, rewTitle1: 'T1', rewTitle2: 'T2', rew1: 'Nada', rew2: 'Nada' },
  a4: { show: false, name: 'First Human Kill!', desc: 'Some Info', tier: 1, diff: 1, exp: 50, rewTitle1: 'T1', rewTitle2: 'T2', rew1: 'Nada', rew2: 'Nada' },
  a5: { show: false, name: 'Title', desc: 'Some Info', tier: 1, diff: 1, exp: 50, rewTitle1: 'T1', rewTitle2: 'T2', rew1: 'Nada', rew2: 'Nada' },
  a6: { show: false, name: 'Title', desc: 'Some Info', tier: 1, diff: 1, exp: 50, rewTitle1: 'T1', rewTitle2: 'T2', rew1: 'Nada', rew2: 'Nada' }
}
</script>
