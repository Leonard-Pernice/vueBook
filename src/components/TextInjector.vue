<template>
    <div ref="container">
      <div :id="props.p.id">
        <p v-if="props.p.attributes === ''" class="text-justify py-1 px-4 text-sm indent-3 leading-6 text-yellow-50">{{ props.p.text }}</p>
        <p v-if="props.p.attributes === 'apUsed'"></p>
        <p v-if="props.p.attributes === 'mpUsed'"></p>
        <p v-if="props.p.attributes === 'stUsed'"></p>
        <p v-if="props.p.attributes === 'dmgtaken'"></p>
        <p v-if="props.p.attributes === 'stim'"></p>
        <div v-if="props.p.attributes === 'monster'"><killMsg :p="props.p"></killMsg></div>
        <div v-if="props.p.attributes === 'levelup'"><LevelUp :p="props.p"></LevelUp></div>
        <div v-if="props.p.attributes === 'achievement'"><AchievementMsg :p="props.p"></AchievementMsg></div>
        <div v-if="props.p.attributes === 'quest'"><QuestMsg :p="props.p"></QuestMsg></div>
        <div v-if="props.p.attributes === 'item'"><ItemMsg :p="props.p"></ItemMsg></div>
      </div>
    </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useNavigationStore } from '@/store/index'
import { useChapterStore } from '@/store/chapter'

import killMsg from '@/components/killMsg.vue'
import AchievementMsg from '@/components/AchievementMsg.vue'
import QuestMsg from '@/components/QuestMsg.vue'
import LevelUp from '@/components/LevelUp.vue'
import ItemMsg from '@/components/ItemMsg.vue'

const props = defineProps({
  p: {
    type: Object,
    default: () => ({})
  }
})

const chapterStore = useChapterStore()
const navigationStore = useNavigationStore()
const container = ref()

onMounted(() => {
  if (props.p.attributes != '') {
    // const pElements = container.value.querySelectorAll('div')
    const p = document.getElementById(props.p.id)
    // console.log('ID:', props.p.id)
    const height = parseInt(Math.floor(p.offsetTop) - window.innerHeight / 2)
    navigationStore.eventParagraphHeights[height] = props.p.id
    chapterStore.eventParagraphs[props.p.id] = props.p
    chapterStore.eventParagraphs[props.p.id]['relatedEvent'] = searchEvent(props.p.id)
    // console.log(chapterStore.paragraphs[props.p.id])
  }
  const pH = document.getElementById(props.p.id)
  const pHeight = parseInt(Math.floor(pH.offsetTop) - window.innerHeight / 2)
  navigationStore.paragraphHeights[pHeight] = props.p.id
})

function searchEvent (reference) {
  const result = []
  const events = [
    chapterStore.characters,
    chapterStore.players,
    chapterStore.stats,
    chapterStore.skills,
    chapterStore.relationships,
    chapterStore.achievements,
    chapterStore.quests,
    chapterStore.inventories,
    chapterStore.slots,
    chapterStore.equipments,
    chapterStore.items,
    chapterStore.currencies
  ]
  for (const event in events) {
    const eventList = Object.values(events[event])
    const relatedEvent = eventList.filter(item => item.referenceParagraph === reference)
    if (relatedEvent != []) {
      result.push(...relatedEvent)
    }
  }
  return result
}

</script>
