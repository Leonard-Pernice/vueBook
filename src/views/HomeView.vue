<template>
  <div v-if="errMsg"> {{ errMsg }} </div>
  <KeepAlive>
    <Suspense>
      <ChapterContent />
      <template #fallback>
        <LoadingScreen />
      </template>
    </Suspense>
  </KeepAlive>
</template>

<script setup>
import { ref, onErrorCaptured, watchEffect, onMounted } from 'vue'
import { useNavigationStore } from '@/store/index'
import { useChapterStore } from '@/store/chapter'
import { useEventListener } from '@vueuse/core'
import LoadingScreen from '@/components/LoadingScreen.vue'
import ChapterContent from '@/views/ChapterContent.vue'

const navigationStore = useNavigationStore()
const chapterStore = useChapterStore()
const pastEvents = []
const futureEvents = []

const errMsg = ref(null)
const scrolling = ref(false)

onErrorCaptured(() => {
  errMsg.value = 'Error loading chapter'
  console.log(errMsg.value)
})

onMounted(async () => {
  console.log(localStorage.getItem('savedScrollPosition'))
  if (localStorage.getItem('savedScrollPosition') > 0) {
    scrolling.value = true
    try {
      console.log('Chapter still loading...')
      await waitForChapter(checkLoadStatus)
      console.log('Now scrolling...')
      scrollTo()
    } catch (error) {
      console.log(error)
    }
    scrolling.value = false
  }
})

async function waitForChapter(checkLoadStatus) {
  while (checkLoadStatus()) {
    await delay (100)
  }
}

const checkLoadStatus = () => {
  return chapterStore.dataLoaded
}

function delay(ms) {
  return new Promise(resolve => setTimeout(resolve, ms))
}

watchEffect(() => {
  console.log(navigationStore.savedScrollPosition)
  localStorage.setItem('savedScrollPosition', navigationStore.savedScrollPosition)
})

useEventListener(document, 'scroll', () => {
  if (chapterStore.dataLoaded === true && !scrolling.value) {
    findClosestParagraph()
    console.log('Closest Paragraph: ', navigationStore.savedScrollPosition)
    console.log('In Local Storage: ', localStorage.getItem('savedScrollPosition'))
  }
  const currentScrollPosition = window.scrollY || document.documentElement.scrollTop
  if (currentScrollPosition < 0) {
    return
  }
  if (Math.abs(currentScrollPosition - navigationStore.lastScrollPosition) < 60) {
    return
  }
  if (currentScrollPosition < navigationStore.lastScrollPosition) {
    navigationStore.toggleTopNav()
  } else {
    navigationStore.hideTopNav()
  }
  navigationStore.lastScrollPosition = currentScrollPosition
  if (futureEvents.length === 0 && pastEvents.length === 0) {
    futureEvents.push(...Object.values(chapterStore.eventParagraphs))
  }
  const latestParagraph = chapterStore.paragraphs[findClosestLower(navigationStore.eventParagraphHeights, navigationStore.lastScrollPosition)]
  if (latestParagraph) {
    const indexFutureEvent = futureEvents.findIndex(item => item.id === latestParagraph.id)
    if (indexFutureEvent >= 0) {
      const processedEvents = futureEvents.splice(0, indexFutureEvent + 1)
      for (const event in processedEvents) {
        assumeEventState(processedEvents[event])
        pastEvents.push(processedEvents[event])
      }
    }
    
    const indexPastEvent = pastEvents.findIndex(item => item.id === latestParagraph.id)
    if (indexPastEvent >= 0 && indexPastEvent < pastEvents.length - 1) {
      console.log('Resetting')
      chapterStore.assumeInitialState()
      const deProcessedEvents = pastEvents.splice(indexPastEvent + 1, pastEvents.length)
      futureEvents.unshift(...deProcessedEvents)
      for (const event in pastEvents) {
        assumeEventState(pastEvents[event])
      }
    }

    // Next Steps:
    //   o create component for showing equipment
    //   o simplify the components by adapting everything to the same structure as the database
    //     -> then I only have to change the pointer, not all the values inside

  } else if (latestParagraph === undefined && pastEvents.length > 0) {
    console.log('Resetting')
    chapterStore.assumeInitialState()
    futureEvents.unshift(pastEvents.pop())
  }
})

function assumeEventState (event) {
  console.log('Processing: new event!', event.attributes)
  // console.log(event)
  for (const relevantEvent of event.relatedEvent) {
    if (event.attributes === 'levelup') {
      console.log(chapterStore.current.stats)
      handleLevelUp(relevantEvent)
    }
    switch (relevantEvent.typeReference) {
      case 'item':
        handleItem(relevantEvent)
        break
      case 'player':
        handleKill(relevantEvent)
        break
      case 'levelup':
        console.log(relevantEvent)
        
        break
      case 'quest':
        handleQuest(relevantEvent)
        break
      case 'achievement':
        handleAchievement(relevantEvent)
        break
      case 'stat':
        handleStat(relevantEvent)
        break
      default:
        break
    }
  }
}

function handleStat (stat) {
  const statIndex = chapterStore.current.stats.findIndex(s => s.name === stat.name)
  showStat(stat)
  if (chapterStore.current.stats.includes(stat)) {
    return
  } else {
    if (statIndex >= 0) {
      chapterStore.current.stats[statIndex] = stat
      console.log('Updating stats with: ', stat.name)
    } else {
      chapterStore.current.stats.push(stat)
      console.log('Updating stats with: ', stat.name)
    }
  }
}

function handleAchievement (achievement) {
  if (chapterStore.current.achievements.includes(achievement)) {
    return
  } else {
    chapterStore.current.achievements.push(achievement)
  }
  console.log('Updating achievements with achievement: ', achievement.name)
}

function handleQuest (quest) {
  const questIndex = chapterStore.current.quests.findIndex(q => q.name === quest.name)
  if (questIndex >= 0) {
    chapterStore.current.quests[questIndex] = quest
  } else {
    chapterStore.current.quests.push(quest)
  }
  console.log('Updating quests with quest: ', quest.name)
}

function handleKill (player) {
  chapterStore.currentPlayer = player
  console.log('Updating player: ', chapterStore.currentPlayer)
}

function handleItem (item) {
  // Checking Inventory
  if (item.inInventory) {
    if (!chapterStore.current.inventories.includes(item)) {
      chapterStore.current.inventories.push(item)
      console.log('Updating inventory with item: ', item.name)
    }
  }
  if (!item.inInventory && getNames(chapterStore.current.inventories).includes(item.name)) {
    chapterStore.current.inventories = chapterStore.current.inventories.filter(remain => remain !== item)
  }
  // Checking Equipment
  let slotCounts = {
    "Head": 0,
    "Neck": 0,
    "Shoulders": 0,
    "Back": 0,
    "Chest": 0,
    "Wrist": 0,
    "Waist": 0,
    "Underpants": 0,
    "Legs": 0,
    "Feet": 0,
    "Hand": -1,
    "Ring": -9,
    "Trinket": 0,
    "Ranged": 0,
    "Earring": -1
  }
  chapterStore.current.equipments.forEach(equip => {
    const slot = equip.slot
    if (slot in slotCounts) {
      slotCounts[slot]++
    } else { throw new Error(`This slot does not exist, ${equip}`)}
  })
  console.log('Slot counts: ', slotCounts)
  if (item.isEquipped) {
    if (!chapterStore.current.equipments.includes(item)) {
      if (slotCounts[item.slot] <= 0) {
        const itemIndex = chapterStore.current.equipments.findIndex(equip => equip.name === item.name)
        if (itemIndex >= 0) {
          chapterStore.current.equipments[itemIndex] = item
          console.log('Updating equipment with item: ', item.name)
        } else {
          chapterStore.current.equipments.push(item)
          console.log('Updating equipment with item: ', item.name)
        }
      } else { throw new Error(`Too many items of slot "${item.slot}" already equipped. Cannot equip ${item}`)}
    }
  }
  if (!item.isEquipped && getNames(chapterStore.current.equipments).includes(item.name)) {
    chapterStore.current.equipments = chapterStore.current.equipments.filter(remain => remain !== item)
  }
}

function handleLevelUp (levelup) {
  console.log(levelup)
}

function getNames(arr) {
  let names = arr.map(obj => obj.name)
  return names
}


function scrollTo () {
  const paragraph = localStorage.getItem('savedScrollPosition')
  const element = document.getElementById(paragraph)
  const rect = element.getBoundingClientRect()
  console.log('Trying to scroll to paragraph:', paragraph)
  window.scrollTo({
    left: rect.left + window.scrollX, 
    top: rect.top + window.scrollY, 
    behavior: 'smooth'
  })
  navigationStore.hideTopNav()
}

// function getLowestNumberedParagraph(paragraphs) {
//     const keys = Object.keys(paragraphs);
//     let minNum = Infinity;
//     let minKey = "";

//     keys.forEach(key => {
//         let num = parseInt(key.split("_")[0]);
//         if (num < minNum) {
//             minNum = num;
//             minKey = key;
//         }
//     });

//     return minKey;
// }

function findClosestLower (dictionary, searchValue) {
  const array = Object.keys(dictionary).map(Number)
  let left = 0
  let right = array.length - 1
  
  while (left <= right) {
    const mid = Math.floor((left + right) / 2)
    if (array[mid] === searchValue) {
      return dictionary[array[mid - 1]]
    } else if (array[mid] < searchValue) {
      left = mid + 1
    } else {
      right = mid - 1
    }
  }

  return dictionary[array[right]]
}

function copySurfaceData(inputObj) {
    const outputObj = {};

    for (const key in inputObj) {
        const value = inputObj[key];

        if (value !== null && typeof value === 'object') {
            // We skip objects (including arrays)
            continue
        }

        outputObj[key] = value;
    }

    return outputObj;
}

function insertSurfaceData (obj, key) {
  const newObj = {}
  const inners = obj[key]
  // console.log(inners)
  if (inners) {
    for (const [, inner_value] of Object.entries(inners)) {
      const newKey = `${inner_value.referenceParagraph}_${inner_value.name}`
      newObj[newKey] = inner_value
    }
  }
  // console.log(newObj)
  return newObj
}

function insertDeepData (obj, key) {
  const newObj = {}
  for (const [, outer_value] of Object.entries(obj)) {
    const inners = outer_value[key]
    if (inners) {
      for (const [, inner_value] of Object.entries(inners)) {
        const newKey = `${inner_value.referenceParagraph}_${inner_value.name}`
        newObj[newKey] = inner_value
      }
    }
  }
  return newObj
}



function segregateStores (obj) {
  // console.log(obj)
  // Characters
  chapterStore.characters = {}
  // console.log(chapterStore.characters)
  chapterStore.characters = insertSurfaceData(obj, 'characters')
  // console.log(chapterStore.characters)
  // Players
  chapterStore.players = {}
  chapterStore.players = insertDeepData(obj['characters'], 'players')
  // Stats
  chapterStore.stats = {}
  chapterStore.stats = insertDeepData(chapterStore.players, 'stats')
  // Skills
  chapterStore.skills = {}
  chapterStore.skills = insertDeepData(chapterStore.players, 'skills')
  // Items
  chapterStore.items = {}
  chapterStore.items = insertDeepData(obj['characters'], 'items')
  // Relationships
  chapterStore.relationships = {}
  chapterStore.relationships = insertDeepData(chapterStore.players, 'relationships')
  // Achievements
  chapterStore.achievements = {}
  chapterStore.achievements = insertDeepData(chapterStore.players, 'achievements')
  // Quests
  chapterStore.quests = {}
  chapterStore.quests = insertDeepData(chapterStore.players, 'quests')
  // // Inventories
  // chapterStore.inventories = {}
  // chapterStore.inventories = insertDeepData(chapterStore.players, 'inventories')
  // // Slots
  // chapterStore.slots = {}
  // chapterStore.slots = insertDeepData(chapterStore.inventories, 'slots')
  // // Equipments
  // chapterStore.equipments = {}
  // chapterStore.equipments = insertDeepData(chapterStore.players, 'equipments')
  // Currencies
  chapterStore.currencies = {}
  chapterStore.currencies = insertDeepData(chapterStore.players, 'currencies')

  // console.log(chapterStore.items)

  // const result = {}

  // function recurse (cur, prop) {
  //   if (Object(cur) !== cur) {
  //     result[prop] = cur
  //   } else if (Array.isArray(cur)) {
  //     const l = cur.length
  //     for (let i = 0; i < l; i++) {
  //       recurse(cur[i], prop + '[' + i + ']')
  //     }
  //     if (l === 0) {
  //       result[prop] = []
  //     }
  //   } else {
  //     let isEmpty = true
  //     for (const p in cur) {
  //       isEmpty = false
  //       recurse(cur[p], prop ? prop + '.' + p : p)
  //     }
  //     if (isEmpty && prop) {
  //       result[prop] = {}
  //     }
  //   }
  // }
  // recurse(obj, '')

  // return result
}

function showStat (stat) {
  const validBars = ['Vitality', 'Momentum', 'Charisma', 'Spirit']
  if (validBars.includes(stat.name) && calcTotal(stat) > 0) {
    navigationStore.bars[stat.name] = true
  } else {
    navigationStore.bars[stat.name] = false
  }
}

function calcTotal (stat) {
  return Math.floor(stat.base + stat.increased + Math.floor(parseFloat(stat.trained)))
}

const findClosestParagraph = () => {
  const scrollPosition = window.scrollY - window.outerHeight - 78
  const paragraphHeights = navigationStore.paragraphHeights

  let closestDistance = Infinity
  let closestId = null

  const heightEntries = Object.entries(paragraphHeights)
  const numEntries = heightEntries.length

  let left = 0
  let right = numEntries - 1

  while (left <= right) {
    const mid = Math.floor((left + right) / 2)
    const [height, paragraphId] = heightEntries[mid]

    const heightValue = parseInt(height)
    const distance = Math.abs(scrollPosition - heightValue)

    if (distance < closestDistance) {
      closestDistance = distance
      closestId = paragraphId
    }

    if (heightValue === scrollPosition) {
      // Exact match found, no need to continue searching
      break
    } else if (heightValue < scrollPosition) {
      left = mid + 1
    } else {
      right = mid - 1
    }
  }

  navigationStore.savedScrollPosition = closestId
}


</script>
