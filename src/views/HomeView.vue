<template>
  <div class="mt-20 mx-4 flex flex-col items-center justify-center">
    <img class="max-w-[90%] h-auto my-4" src="@/assets/img/chapterheads/chapter1.jpg" alt="Cityview">
    <!-- <figure class="align-center border-2 border-white">
      <img :src="chapter.get_image">
    </figure> -->
    <h1 class="text-white text-2xl">Chapter {{ chapterStore.currentChapter }}</h1>
    <div v-for="(textObj, i) in chapterStore.paragraphs" :key="i" :id="textObj.id"><TextInjector :p="textObj"></TextInjector></div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useNavigationStore } from '@/store/index'
import { useChapterStore } from '@/store/chapter'
import { useEventListener } from '@vueuse/core'
import TextInjector from '@/components/TextInjector.vue'
import axios from 'axios'

const navigationStore = useNavigationStore()
const chapterStore = useChapterStore()
const pastEvents = []
const futureEvents = []

onMounted(() => {
  navigationStore.showTopNav = true
  getCurrentChapter()
})



async function getCurrentChapter () {
  await axios
    .get('/api/v1/chapter/1/') // + chapterStore.currentChapter.chapterNumber + '/'
    .then(response => {
      const entries = response.data[0]
      const numericKey = /^\d+$/
      const { data, paragraphs } = Object.keys(entries).reduce(
        (acc, key) => {
          if (numericKey.test(key)) {
            acc.paragraphs[key] = entries[key]
          } else {
            acc.data[key] = entries[key]
          }
          return acc
        },
        { data: {}, paragraphs: {} }
      )
      // const names = ['characters', 'players', 'stats', 'skills', 'relationships', 'achievements', 'quests', 'inventories', 'slots', 'equipments', 'items', 'currencies']
      chapterStore.chapter = segregateStores(data)
      // console.log(chapterStore.chapter)
      chapterStore.paragraphs = paragraphs
      document.title = 'Book | ' + chapterStore.chapter.name
      chapterStore.currentChapter = chapterStore.chapter.name.replace(/[^0-9]/g, '')
      console.log('Current Chapter is: ', chapterStore.currentChapter)
      assumeInitialState()
    })
    .catch(error => {
      console.log(error)
    })
}

useEventListener(document, 'scroll', () => {
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
  const latestParagraph = chapterStore.paragraphs[findClosestLower(navigationStore.paragraphHeights, navigationStore.lastScrollPosition)]
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
      assumeInitialState()
      const deProcessedEvents = pastEvents.splice(indexPastEvent + 1, pastEvents.length)
      futureEvents.unshift(...deProcessedEvents)
      for (const event in pastEvents) {
        assumeEventState(pastEvents[event])
      }
    }

    // Next Steps:
    // x create list of only event paragraphs
    //   x should only be created once, but inside this function
    // x iterate backwards (high- to low key) and update data
    // o create functions for each type of event / update
    //   o first event is "item" --> need to create inventory / slot / equipment events for this to ensure coherence & integrity
    //   o currently my get methods don't return the @property attributes. change to fields???
    //   o simplify the process by adapting everything to the same structure as the database
    //     -> then I only have to change the pointer, not all the values inside
    // x ensure the initialState is updated before each time an event is called to ensure the right eventStates are assumed

  } else if (latestParagraph === undefined && pastEvents.length > 0) {
    assumeInitialState()
    futureEvents.unshift(pastEvents.pop())
  }
})

function assumeInitialState () {
  console.log('INITIALIZING!')
  const listOfStates = [
    [chapterStore.currentPlayer, chapterStore.players],
    [chapterStore.currentStats, chapterStore.stats],
    [chapterStore.currentSkills, chapterStore.skills],
    [chapterStore.currentQuests, chapterStore.quests],
    [chapterStore.currentAchievements, chapterStore.achievements],
    [chapterStore.currentPact, chapterStore.pacts],
    [chapterStore.currentParagon, chapterStore.paragons]
  ]
  for (const state in listOfStates) {
    // console.log(state)
    const keys = Object.keys(listOfStates[state][1])
    listOfStates[state][0] = listOfStates[state][1][keys[0]]
    // console.log(listOfStates[state][0])
  }
}

function assumeEventState (event) {
  console.log('Processing: new event!', event.attributes)
  console.log(event)
}

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

// function findClosestKey(dictionary, searchValue) {
//   const keys = Object.keys(dictionary).map(Number)
//   let left = 0
//   let right = keys.length - 1
//   while (left <= right) {
//     const middle = Math.floor((left + right) / 2)
//     const diff = Math.abs(keys[middle] - searchValue)
//     if (keys[middle] === searchValue && diff < 200) {
//       return dictionary[keys[middle]]
//     } else if (keys[middle] > searchValue) {
//       right = middle - 1
//     } else {
//       left = middle + 1
//     }
//     if (keys[middle] >= searchValue && keys[middle - 1] <= searchValue) {
//       if (Math.min(Math.abs(keys[middle] - searchValue), Math.abs(keys[middle - 1] - searchValue)) < 200) {
//         return (searchValue - keys[middle - 1] < keys[middle] - searchValue) ? dictionary[keys[middle - 1]] : dictionary[keys[middle]]
//       }
//     }
//   }
//   if (right < 0 && Math.abs(keys[right + 1] - searchValue) < 200) {
//     return dictionary[keys[left]]
//   } else if (left >= keys.length && Math.abs(keys[left - 1] - searchValue) < 200) {
//     return dictionary[keys[right]]
//   } else if (Math.min(Math.abs(keys[right] - searchValue), Math.abs(keys[left] - searchValue)) < 200) {
//     return searchValue - keys[right] < keys[left] - searchValue ? dictionary[keys[right]] : dictionary[keys[left]]
//   } else {
//     return null
//   }
// }


// function findClosestKey(dictionary, searchValue) {
//   const keys = Object.keys(dictionary).map(Number)
//   let left = 0
//   let right = keys.length - 1
//   while (left <= right) {
//     const middle = Math.floor((left + right) / 2)
//     // console.log('testing if', keys[middle], ' > ', searchValue)
//     if (keys[middle] === searchValue) {
//       return dictionary[keys[middle]]
//     } else if (keys[middle] > searchValue) {
//       right = middle - 1
//     } else {
//       left = middle + 1
//     }
//     if (keys[middle] >= searchValue && keys[middle - 1] <= searchValue) {
//       return (searchValue - keys[middle - 1] < keys[middle] - searchValue) ? dictionary[keys[middle - 1]] : dictionary[keys[middle]]
//     }
//   }
//   if (right < 0) {
//     return dictionary[keys[left]]
//   } else if (left >= keys.length) {
//     return dictionary[keys[right]]
//   } else if (searchValue - keys[right] < keys[left] - searchValue) {
//     return dictionary[keys[right]]
//   } else {
//     return dictionary[keys[left]]
//   }
// }


function insertSurfaceData (obj, key) {
  const newObj = {}
  const inners = obj[key]
  if (inners) {
    for (const [, inner_value] of Object.entries(inners)) {
      const newKey = `${inner_value.referenceParagraph}_${inner_value.name}`
      newObj[newKey] = inner_value
    }
  }
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

  // Items
  chapterStore.items = {}
  chapterStore.items = insertSurfaceData(obj, 'items')
  // Characters
  chapterStore.characters = {}
  chapterStore.characters = insertSurfaceData(obj, 'characters')
  // Players
  chapterStore.players = {}
  chapterStore.players = insertDeepData(obj['characters'], 'players')
  // Stats
  chapterStore.stats = {}
  chapterStore.stats = insertDeepData(chapterStore.players, 'stats')
  // Skills
  chapterStore.skills = {}
  chapterStore.skills = insertDeepData(chapterStore.players, 'skills')
  // Relationships
  chapterStore.relationships = {}
  chapterStore.relationships = insertDeepData(chapterStore.players, 'relationships')
  // Achievements
  chapterStore.achievements = {}
  chapterStore.achievements = insertDeepData(chapterStore.players, 'achievements')
  // Quests
  chapterStore.quests = {}
  chapterStore.quests = insertDeepData(chapterStore.players, 'quests')
  // Inventories
  chapterStore.inventories = {}
  chapterStore.inventories = insertDeepData(chapterStore.players, 'inventories')
  // Slots
  chapterStore.slots = {}
  chapterStore.slots = insertDeepData(chapterStore.inventories, 'slots')
  // Equipments
  chapterStore.equipments = {}
  chapterStore.equipments = insertDeepData(chapterStore.players, 'equipments')
  // Currencies
  chapterStore.currencies = {}
  chapterStore.currencies = insertDeepData(chapterStore.players, 'currencies')

  // console.log(chapterStore.items)

  const result = {}

  function recurse (cur, prop) {
    if (Object(cur) !== cur) {
      result[prop] = cur
    } else if (Array.isArray(cur)) {
      const l = cur.length
      for (let i = 0; i < l; i++) {
        recurse(cur[i], prop + '[' + i + ']')
      }
      if (l === 0) {
        result[prop] = []
      }
    } else {
      let isEmpty = true
      for (const p in cur) {
        isEmpty = false
        recurse(cur[p], prop ? prop + '.' + p : p)
      }
      if (isEmpty && prop) {
        result[prop] = {}
      }
    }
  }
  recurse(obj, '')

  return result
}

</script>