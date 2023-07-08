<template>
  <div class="flex items-center justify-center my-8">
    <div class="w-96 bg-gradient-radial from-gr-inner-blue to-gr-outer-blue text-white text-center">
      <div class="border-white border-y border-x m-2">
        <div class="flex justify-center">
          <div class="relative inline-block w-full h-14">
            <div class="absolute block -inset-x-14 -inset-y-8 bg-lying-s bg-repeat-x bg-center"></div>
          </div>
          <div class="relative inline-block w-full h-14">
            <div class="absolute block -inset-x-14 -inset-y-8 bg-lying-y bg-no-repeat bg-center"></div>
          </div>
          <div class="relative inline-block w-full h-14">
            <div class="absolute block -inset-x-14 -inset-y-8 bg-lying-s bg-repeat-x bg-center"></div>
          </div>
        </div>
        <div class="text-xl border-b border-white mx-4">
          Achievement:
        </div>

        <div class="my-4"><GlowText :content="relevantAchievement.name"></GlowText></div>
        <div class="border-y border-white my-2 px-2">
          {{ relevantAchievement.description }}
        </div>
        <div class="my-4"><GlowText :content="`EXP Reward: ${(props.p.exp*100).toString()}%`"></GlowText></div>
        <div v-show="relevantAchievement.reward != 'Insert Reward here!'">
          <div class="pt-2 border-t border-white">Additional Reward: </div>
          <div class="mt-4 mb-6"><GlowText :content="relevantAchievement.reward"></GlowText></div>
        </div>
        
        <div class="flex justify-center">
          <div class="relative inline-block w-full h-8">
            <div class="absolute block -inset-x-14 -inset-y-8 bg-lying-knife bg-no-repeat bg-center"></div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <!-- <div>{{ props.p.text }} {{ calcKillExp(props.p) }}</div> -->
</template>

<script setup>
import { useChapterStore } from '@/store/chapter'
import GlowText from '@/components/GlowText.vue'
import { findEvent } from '@/help/extraFunctions.js'

const chapterStore = useChapterStore()

const props = defineProps({
  p: {
    type: Object,
    default: () => ({})
  }
})

const relevantAchievement = findEvent(chapterStore.achievements, props.p.id)


</script>
