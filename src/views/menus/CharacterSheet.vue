<template>
  <div class="relative mt-16 mx-4 md:mt-24 bg-gradient-radial from-gr-inner-blue to-gr-outer-blue text-white">
    <div class="mx-6">
    <div class="flex justify-center">
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
    <div class="flex justify-center">
      <div class="relative inline-block w-full">
      </div>
      <div name="CharacterNameANDTitle" class="flex justify-center w-full h-8 text-center mt-4 text-[1rem] md:h-12 md:text-[1.5rem]">
        <div class="w-screen"><GlowText :content="combineNameTitle(chapterStore.currentPlayer)"></GlowText></div>
      </div>
      <div class="relative inline-block w-full h-14">
      </div>
    </div>
    <div name="CharacterLevelANDSpeccANDClass" class="flex justify-center">
      <div class="flex justify-center h-4 w-full text-center text-xs">
        <GlowText :content="combineLevelSpeccClass(chapterStore.currentPlayer)"></GlowText>
      </div>
    </div>
    <div name="POWER" class="flex justify-center">
      <div class="flex justify-center h-4 w-full text-center text-xl my-3">
        <GlowText :content="'Power: ' + calculatePower(chapterStore.current.stats)"></GlowText>
      </div>
    </div>
    <div class="border grid grid-cols-4 lg:grid-cols-8 m-1 p-1">
      <div class="border-y-2 py-1 flex flex-row col-span-4 lg:col-span-8">
        <div name="LEVEL" class="flex h-6 w-32 text-lg">
          <GlowText :content="'Level: ' + chapterStore.currentPlayer.level"></GlowText>
        </div>
        <div name="EXP %" class="flex h-6 w-32 text-xs">
          <GlowText :content="'Experience: ' + chapterStore.currentPlayer.exp + '%'"></GlowText>
        </div>
        <div name="EXP BAR" class="flex grow h-full bg-gray-200">
          <div class="h-inherit bg-blue-600 text-xs font-medium text-blue-100 text-center p-0.5 leading-none" :style="{ width: (chapterStore.currentPlayer.exp)+'%' }"></div>
        </div>
      </div>
      <div class="border-b-2 py-1 flex justify-center w-full h-6 text-center text-xs lg:col-span-2">
        {{ chapterStore.currentPlayer.typ }}
      </div>
      <div class="border-b-2 py-1 flex justify-center w-full h-6 text-center text-xs lg:col-span-2">
        {{ chapterStore.currentCharacter.species }}
      </div>
      <div class="border-b-2 py-1 flex justify-center w-full h-6 text-center text-xs lg:col-span-2">
        {{ chapterStore.currentCharacter.gender }}
      </div>
      <div class="border-b-2 py-1 flex justify-center w-full h-6 text-center text-xs lg:col-span-2">
        {{ chapterStore.currentCharacter.age }}
      </div>
    </div>
    <div name="STAT FOR LOOP" class="m-1" v-for="(stat, i) in chapterStore.current.stats" :key="i">
      <div class="border grid grid-cols-4 lg:grid-cols-9">
        <StatToolTip :stat="stat" placement="right">
          <div name="STAT NAME" class="pt-1 flex justify-center w-full h-6 text-center text-xs z-20 hover:bg-blue-900">
            {{ stat.name }}
          </div>
        </StatToolTip>
        <div name="STAT BAR VALUE" class="flex justify-center p-0.5 w-full text-center h-6 col-span-3">
          <div name="STAT BAR" class="relative col-span-3 lg:col-span-7 w-full bg-slate-800 text-black">
            <div
              class="absolute inline-block left-0 h-full text-xs text-center border border-blue-300"
              :style="{ width: (stat.bar === 0 ? ('-') : (stat.bar/(getTotal(stat))*100).toFixed(0)+'%'),
              'background-color': stat.bar === 0 ? ('black') : (getColor(stat)) }">
            </div>
            <div class="absolute inline-block top-[10%] left-2 text-xs text-white">{{ stat.bar }}</div>
          </div>
        </div>
        <div name="STAT VALUE" class="flex justify-center h-6 text-center text-xs">{{ getTotal(stat) }}</div>
        <div name="STAT MAX" class="px-0.5 pb-0.5 h-6 w-full text-center text-xs col-span-3 lg:col-span-4">
          <div class="grid grid-cols-10 h-full">
            <div v-for="(s, j) in 10" :key="j" class="border-blue-900 border" :style="{ 'background-color': (returnTileColor(stat, chapterStore.currentPlayer, chapterStore.currentCharacter, s)) }"></div>
          </div>
        </div>
      </div>
    </div>
      <div class="flex justify-center w-full h-6 text-center text-sm ">
        <GlowText :content="'Unspent Statpoints: ' + getRemainingStatPoints(chapterStore.currentPlayer, chapterStore.current.stats)"></GlowText>
      </div>
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
  </div>
</template>

<script setup>
import GlowText from '@/components/GlowText.vue'
import { calcAccumulatedStatPoints, statAbreviations } from '@/help/extraFunctions.js'
import { useChapterStore } from '@/store/chapter'
import statMulti from '@/help/statMulti.json'
import { useNavigationStore } from '@/store/index'
import { onMounted } from 'vue'
import StatToolTip from '@/components/StatToolTip.vue'
import axios from 'axios'

const chapterStore = useChapterStore()
const navigationStore = useNavigationStore()
const statMultipliers = statMulti

onMounted(() => {
  navigationStore.changeActivePage()
  if (chapterStore.dataLoaded === false) {
    getCurrentChapter(navigationStore.chapterNumber) // navigationStore.chapterNumber
  }
})

async function getCurrentChapter (chapterNumber) {
  await axios
    .get(`/api/v1/chapter/${chapterNumber}/`)
    .then(response => {
      chapterStore.processChapter(response.data[0])
      console.log('Current Chapter is: ', chapterStore.currentChapter)
    })
    .catch(error => {
      console.log(error)
    })
}

if (chapterStore.initialized === false) {
  chapterStore.assumeInitialState()
  // console.log(chapterStore.currentCharacter)
}

function combineNameTitle (player) {
  if ((''+player.title).includes('the')) {
    return player.name + player.title
  } else if (player.title === '-') {
    return player.name
  }
  return player.title + player.name
}

function combineLevelSpeccClass (player) {
  if ((player.specc === '-' && player.class === '-') || (player.specc === null && player.class === null)) {
    return 'Level ' + player.level
  } else if (player.class != null && player.class != '-') {
    return 'Level' + player.level + ' ' + player.class
  }
}

function getTotal (stat) {
  return stat.base + stat.increased + Math.floor(stat.trained)
}

function calculatePower (stats) {
  let power = 0
  for (const stat of stats) {
    let total = getTotal(stat)
    power += parseInt(total)
  }
  return power
}

function getColor (stat) {
  const colors = {
    'Vitality': 'red',
    'Strength': '#5c0da6',
    'Agility': '#02edd6',
    'Spirit': 'blue',
    'Momentum': 'green',
    'Charisma': 'pink'
  }
  return colors[stat.name]
}

function getStatMaximum (stat, player, character) {
  let totalStatPoints = calcAccumulatedStatPoints(player.level)
  if (totalStatPoints === 0) {
    totalStatPoints = 1
  }
  const genderMulti = parseFloat(statMultipliers[character.species.toLowerCase()][character.gender.toLowerCase()]["baseMult"])
  const statMulti = parseFloat(statMultipliers[character.species.toLowerCase()][character.gender.toLowerCase()][invertedStatAbreviations[stat.name]])
  const maxval = ((totalStatPoints/2 * genderMulti * statMulti)) + parseInt(stat.base)
  // console.log(totalStatPoints)
  // console.log(genderMulti)
  // console.log(statMulti)
  return maxval
  // =(ROUNDUP(VLOOKUP(Level,EXP_AND_STATPOINTS,6,TRUE)/2 <- total stats at level / 2
  //* VLOOKUP("Human",StatLimit,2,FALSE) <- Gender Multi
  //* VLOOKUP("Human",StatLimit,3,FALSE),0) <- Stat Multi
  //+ IF(Level>=10,Level,0)+AP26) <- Base
}

function returnTileColor (stat, player, character, tile) {
  const maxval = getStatMaximum(stat, player, character)
  // console.log(maxval)
  return ((maxval === 0) ? ('white') : (getTotal(stat) / maxval >= (tile / 10)) ? ('#4169E1') : ('transparent'))
}

function getRemainingStatPoints (player, stats) {
  const totalStatPoints = calcAccumulatedStatPoints(player.level)
  let spentStatPoints = 0
  // console.log(stats)
  for (const stat of stats) {
    spentStatPoints += stat.increased
  }
  const remainingStatPoints = totalStatPoints - spentStatPoints
  return remainingStatPoints
}

// const placeholder = {
//   stat1: ['Vit', 50, '-', 25, 65, 'red'],
//   stat2: ['Str', 28, '-', 28, 65, 'white'],
//   stat3: ['Agi', 38, '-', 38, 65, 'white'],
//   stat4: ['Sp', 0, '-', 0, 0, 'blue'],
//   stat5: ['Mom', 3, '-', 2, 3, 'green'],
//   stat6: ['Cha', 2, '-', 2, 3, 'pink']
// }

const invertedStatAbreviations = {}

// Invert the dictionary
for (const key in statAbreviations) {
  const value = statAbreviations[key]
  invertedStatAbreviations[value] = key
}

</script>
