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
        <GlowText :content="'Skills'"></GlowText>
      </div>
    </div>
    <div
      name="SkillCategories"
      class='grid grid-cols-3 gap-2 m-1 p-1'
      :style="{ 'height': calcSkillHeight(basics, actives, passives) * 3.1 + 'rem' }">
      <div class="border-b grid grid-cols-1 text-[1.5rem] text-center h-10 p-1 mx-4">
        <div class="flex justify-center w-full h-10 text-center">
          <GlowText :content="'Basic'"></GlowText>
        </div>
        <div v-for="(baseSkill, i) in basics" :key="i">
          <BaseTooltip :content="baseSkill[2]" placement="right">
            <div class="text-sm py-2 h-10">{{ baseSkill[0] }}</div>
          </BaseTooltip>
        </div>
      </div>
      <div class="border-b grid grid-cols-1 text-[1.5rem] text-center h-10 p-1 mx-4">
        <div class="flex justify-center w-full h-10 text-center">
          <GlowText :content="'Active'"></GlowText>
        </div>
        <div v-for="(baseSkill, i) in actives" :key="i">
          <BaseTooltip :content="baseSkill[2]" placement="right">
            <div class="text-sm py-2 h-10">{{ baseSkill[0] }}</div>
          </BaseTooltip>
        </div>
      </div>
      <div class="border-b grid grid-cols-1 text-[1.5rem] text-center h-10 p-1 mx-4">
        <div class="flex justify-center w-full h-10 text-center">
          <GlowText :content="'Passive'"></GlowText>
        </div>
        <div v-for="(baseSkill, i) in passives" :key="i">
          <BaseTooltip :content="baseSkill[2]" placement="right">
            <div class="text-sm py-2 h-10">{{ baseSkill[0] }}</div>
          </BaseTooltip>
        </div>
      </div>
  </div>
  <div class="border-y col-span-3 text-sm text-center">Unspent Skillpoints: {{ calcAccumulatedStatPoints(chapterStore.currentPlayer.level) }}</div>
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
import GlowText from '@/components/GlowText.vue'
import { useChapterStore } from '@/store/chapter'
import { onMounted } from 'vue'
import { calcAccumulatedStatPoints } from '@/help/extraFunctions'

const chapterStore = useChapterStore()

const basics = ref({})

const actives = ref({})

const passives = ref({})

onMounted(() => {
  for (const skill in chapterStore.current.skills) {
    if (skill.typ === 'Active') {
      actives[skill.name] = skill
    } else if (skill.typ === 'Passive') {
      passives[skill.name] = skill
    } else if (skill.name === 'Basic') {
      basics[skill.name] = skill
    }
  }
})

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
