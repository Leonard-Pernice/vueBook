<template>
  <!-- SKILL SCREEN START -->
  <div class="relative mt-16 mx-auto md:mt-20 h-full bg-gradient-radial from-gr-inner-blue to-gr-outer-blue text-white overflow-x-hidden">
    <div name="topDecoration" class="flex justify-center">
      <div class="relative inline-block w-full h-14">
        <div class="absolute block -inset-x-14 -inset-y-8 bg-lying-s bg-repeat-x bg-center"></div>
      </div>
      <div class="relative inline-block w-full h-14">
        <div class="absolute block -inset-x-14 -inset-y-8 bg-big-swirl bg-no-repeat bg-center"></div>
      </div>
      <div class="relative inline-block w-full h-14">
        <div class="absolute block -inset-x-14 -inset-y-8 bg-lying-s bg-repeat-x bg-center"></div>
      </div>
    </div>
    <div name="SkillsTitle" class="flex justify-center">
      <div class="flex justify-center w-full h-10 text-center my-4 text-[2rem] md:h-12 md:text-[2.5rem]">
        <div class="absolute block text-blue-400 blur-sm">Skills</div>
        <div class="absolute block text-blue-300">Skills</div>
        <div class="absolute block mix-blend-overlay">Skills</div>
      </div>
    </div>
    <div name="SkillCategories"
    class='grid grid-cols-3 gap-2 m-1 p-1'
    :style="{ 'height': calcSkillHeight(placeholderBasic, placeholderActive, placeholderPassive) * 3.1 + 'rem' }">
    <div class="border-b grid grid-cols-1 text-[1.5rem] text-center h-10 p-1 mx-4">
      <div class="flex justify-center w-full h-10 text-center">
        <div class="absolute block text-blue-400 blur-sm">Basic</div>
        <div class="absolute block text-blue-300">Basic</div>
        <div class="absolute block mix-blend-overlay">Basic</div>
      </div>
      <div v-for="(baseSkill, i) in placeholderBasic" :key="i">
        <BaseTooltip :content="baseSkill[2]" placement="right">
          <div class="text-sm py-2 h-10">{{ baseSkill[0] }}</div>
        </BaseTooltip>
      </div>
    </div>
    <div class="border-b grid grid-cols-1 text-[1.5rem] text-center h-10 p-1 mx-4">
      <div class="flex justify-center w-full h-10 text-center">
        <div class="absolute block text-blue-400 blur-sm">Active</div>
        <div class="absolute block text-blue-300">Active</div>
        <div class="absolute block mix-blend-overlay">Active</div>
      </div>
      <div v-for="(baseSkill, i) in placeholderActive" :key="i">
        <BaseTooltip :content="baseSkill[2]" placement="right">
          <div class="text-sm py-2 h-10">{{ baseSkill[0] }}</div>
        </BaseTooltip>
      </div>
    </div>
    <div class="border-b grid grid-cols-1 text-[1.5rem] text-center h-10 p-1 mx-4">
      <div class="flex justify-center w-full h-10 text-center">
        <div class="absolute block text-blue-400 blur-sm">Passive</div>
        <div class="absolute block text-blue-300">Passive</div>
        <div class="absolute block mix-blend-overlay">Passive</div>
      </div>
      <div v-for="(baseSkill, i) in placeholderPassive" :key="i">
        <BaseTooltip :content="baseSkill[2]" placement="right">
          <div class="text-sm py-2 h-10">{{ baseSkill[0] }}</div>
        </BaseTooltip>
      </div>
    </div>
  </div>
  <div class="border-y col-span-3 text-sm text-center">Unspent Skillpoints: {{ c.skillPoints }}</div>
  <div class="flex justify-center">
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
import BaseTooltip from '@/components/BaseTooltip.vue'

const placeholderBasic = {
  skill1: ['Name', 1, 'desc', 1, 1, 'mod'],
  skill6: ['Name', 1, 'desc', 1, 1, 'mod']
}

const placeholderActive = {
  skill1: ['Name', 1, 'desc', 1, 1, 'mod'],
  skill2: ['Name', 1, 'desc', 1, 1, 'mod'],
  skill6: ['Name', 1, 'desc', 1, 1, 'mod']
}

const placeholderPassive = {
  skill1: ['Name', 1, 'desc', 1, 1, 'mod'],
  skill2: ['Name', 1, 'desc', 1, 1, 'mod'],
  skill3: ['Name', 1, 'desc', 1, 1, 'mod'],
  skill6: ['Name', 1, 'desc', 1, 1, 'mod']
}

const c = {
  skillPoints: 1
}

function calcSkillHeight (b, a, p) {
  const xa = parseInt(Object.keys(a).length)
  const xb = parseInt(Object.keys(b).length)
  const xp = parseInt(Object.keys(p).length)
  const x = Math.max(xa, xb, xp)
  return (isNaN(x)) ? Object.keys(b).length : x
}
</script>
