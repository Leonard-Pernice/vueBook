<template>
  <div class="flex items-center justify-center my-8">
    <div class="w-96 bg-gradient-radial from-gr-inner-blue to-gr-outer-blue text-white text-center">
      <div class="border-white border-y border-x m-2">
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
        <div class="text-l border-b border-white pt-2 mx-4">
          {{ relevantQuest.title }}
        </div>
        <div class="my-4 text-xl py-2"><GlowText :content="relevantQuest.name"></GlowText></div>
        <div class="border-y border-white my-2 p-2">
          {{ relevantQuest.description }}
          <div class="pt-2 mb-2" v-if="relevantQuest.optional_reward != ''"><em>Optional Objective:</em><br>{{ relevantQuest.optional_description }}</div>
          <hr>
          <div class="mt-1">Tier: {{ relevantQuest.tier }}</div>
          <div>Difficulty: {{ relevantQuest.difficulty }}</div>
        </div>
        <div class="p-2"> Rewards:
          <div class="my-4 border-y h-10"><GlowText :content="`EXP: ${relevantQuest.exp}%`"></GlowText></div>
          <div v-show="relevantQuest.reward != ''">
            <div class="mt-4 pt-2 mb-6"><GlowText :content="relevantQuest.reward"></GlowText></div>
          </div>
          <div v-show="relevantQuest.optional_reward != ''">
            <div class="pt-2">Optional reward: </div>
            <div class="mt-4 mb-6"><GlowText :content="relevantQuest.optional_reward"></GlowText></div>
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
import { findEvent, findPlayer, calcExp } from '@/help/extraFunctions.js'

const chapterStore = useChapterStore()

const props = defineProps({
  p: {
    type: Object,
    default: () => ({})
  }
})

const relevantQuest = findEvent(chapterStore.quests, props.p.id)
const relevantPlayer = findPlayer(chapterStore.players, relevantQuest.player)
relevantQuest['level'] = relevantPlayer.level
relevantQuest['type'] = 'quest'
relevantQuest['exp'] = calcExp(relevantQuest)
relevantQuest['title'] = questTitle(relevantQuest)

function questTitle (quest) {
  if (quest.statusOfQuest === 'Unlocked') {
    return 'New Quest unlocked:'
  } else if (quest.statusOfQuest === 'Ongoing') {
    return 'Quest updated:'
  } else if (quest.statusOfQuest === 'Completed') {
    return 'Quest completed!'
  } else {
    return 'Quest:'
  }
}

// function calcExp (msg) {
//   const lvl = parseInt(msg.level)
//   const power = parseInt(msg.difficulty)
//   const tier = parseInt(msg.tier)
//   const typ = msg.type
//   const base = 1.00
//   let reward
//   if (typ === 'achievement' || typ === 'quest') {
//     if (lvl === 0) {
//       return base
//     }
//     switch (tier) {
//       case 0:
//         if (lvl === 1) {
//           reward = 0.125
//           return reward
//         }
//         reward = base / 2 / Math.pow(lvl, 2)
//         console.log('Calculated exp is: ', reward)
//         return reward
//       case 1: // power = difficulty!
//         reward = base * base / 3 * Math.pow(power, 2) / Math.pow(lvl, 2) / 45 * lvl
//         return reward
//       default:
//         reward = base * base * Math.pow(power, 2) / Math.pow(lvl, 2)
//         return reward
//     }
//   } else {
//     return 0.00
//   }
// }

// function findQuest () {
//   const result = {}
//   const type = 'quests'
//   const ref = 'referenceParagraph'
//   const number = props.p.id
//   let path = ''
//   for (const entry in chapterStore.chapter) {
//     if (entry.includes(type) && entry.includes(ref)) {
//       if (chapterStore.chapter[entry] === number) {
//         result.referenceParagraph = number
//         const pathSplit = entry.split('.')
//         path = pathSplit.slice(0, pathSplit.length - 1).join('.')
//         break
//       }
//     }
//   }
//   for (const entry in chapterStore.chapter) {
//     if (entry.includes(path)) {
//       const pathSplit = entry.split('.')
//       const key = pathSplit.pop()
//       result[key] = chapterStore.chapter[entry]
//     }
//   }
//   const player = result.player
//   const regMatch = /characters\[\d+\]\.players\[\d+\]\.id/
//   for (const entry in chapterStore.chapter) {
//     if (entry.match(regMatch) && chapterStore.chapter[entry] === player) {
//       const pathSplit = entry.split('.')
//       const pathToLevel = pathSplit.slice(0, pathSplit.length - 1).join('.') + '.level'
//       result.level = chapterStore.chapter[pathToLevel]
//       result.type = 'quest'
//     }
//   }
//   result.exp = (calcExp(result) * 10000).toFixed(2)
//   if (result.statusOfQuest === 'Unlocked') {
//     return 'New Quest unlocked:'
//   } else if (result.statusOfQuest === 'Ongoing') {
//     return 'Quest updated:'
//   } else if (result.statusOfQuest === 'Completed') {
//     result.exp = parseFloat(result.exp_received).toFixed(2)
//     return 'Quest completed!'
//   } else {
//     return 'Quest:'
//   }
//   return result
// }


</script>
