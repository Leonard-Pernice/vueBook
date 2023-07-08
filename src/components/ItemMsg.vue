<template>
  <div class="flex items-center justify-center my-8">
    <div class="w-[90%] bg-gradient-radial from-gr-inner-blue to-gr-outer-blue text-white text-center">
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
        <div class="grid grid-cols-2 gap-2">
          <div class="col-span-2 p-2 text-xl"> <!-- first row spans both columns -->
            <GlowText :content="relevantItem.name"></GlowText></div>
          <div class="col-span-1 border-y px-2"><p>{{ relevantItem.typ }}</p></div>
          <div class="col-span-1 border-y px-2"><p :class="rarityColor">{{ relevantItem.rarity }}</p></div>
          <div class="col-span-2 border-y px-2 text-left"><p class="text-sm">{{ relevantItem.appearance }}</p></div>
          <div class="col-span-2 border-y px-2 text-left"><p class="text-sm">{{ relevantItem.details }}</p></div>
          <div class="col-span-1 border-y px-2"><p>Creator:</p></div>
          <div class="col-span-1 border-y px-2"><p>{{ relevantItem.creator }}</p></div>
          <div v-if="relevantItem.charge" class="col-span-1 border-y px-2"><p>Charge:</p></div>
          <div v-if="relevantItem.charge" class="col-span-1 border-y px-2">
            <div class="w-full border h-3 bg-gray-500">
              <div :style="{ width: relevantItem.charge + '%', height: '100%' }" class="bg-cyan-400"></div>
            </div>
          </div>
          <div class="col-span-1 border-y px-2"><p>Durability:</p></div>
          <div class="col-span-1 border-y px-2 flex items-center justify-center">
            <div class="w-full border h-3 bg-gray-500">
              <div :style="{ width: durability + '%', height: '100%' }" :class="durabilityColor"></div>
            </div>
          </div>
        </div>

        <div class="flex justify-center">
          <div class="relative inline-block w-full h-8">
            <div class="absolute block -inset-x-14 -inset-y-8 bg-lying-sun bg-no-repeat bg-center"></div>
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
import { ref } from 'vue'

const chapterStore = useChapterStore()

const props = defineProps({
  p: {
    type: Object,
    default: () => ({})
  }
})

const rarities = {
  Trash: "text-grey-500",
  Common: "text-white",
  Uncommon: "text-lime-400",
  Rare: "text-blue-500",
  Epic: "text-violet-600",
  Legendary: "text-amber-500",
  Myth: "text-fuchsia-500",
  Artifact: 'text-yellow-200',
  World: 'text-slate-900'
}

const colorBreakPoints = {
  good: 'bg-green-500',
  damaged: 'bg-orange-500',
  broken: 'bg-red-500'
}


const relevantItem = findEvent(chapterStore.items, props.p.id)
const rarityColor = ref(rarities[relevantItem.rarity])
const durability = ref(relevantItem.durability)
const durabilityColor = ref(getDurabilityColor(relevantItem))

function getDurabilityColor (item) {
  if (item.durability > 80) {
    return colorBreakPoints.good
  } else if (item.durability < 80 && item.durability > 30) {
    return colorBreakPoints.damaged
  } else {
    return colorBreakPoints.broken
  }
}

</script>
