<template >
    <div class="mt-20 mx-4 flex flex-col items-center justify-center">
      <img class="max-w-[90%] h-auto my-4" src="@/assets/img/chapterheads/chapter1.jpg" alt="Cityview">
      <!-- <figure class="align-center border-2 border-white">
        <img :src="chapter.get_image">
      </figure> -->
      <h1 class="text-white text-2xl">Chapter {{ chapterStore.currentChapter }}</h1>
      <button @click="scrollTo(navigationStore.savedScrollPosition)">Scroll to location X</button>
      <div v-for="(textObj, i) in chapterStore.paragraphs" :key="i" :id="textObj.id"><TextInjector :p="textObj"></TextInjector></div>
    </div>
</template>

<script setup>
import { onActivated, onMounted } from 'vue'
import { useChapterStore } from '@/store/chapter'
import { useNavigationStore } from '@/store/index'
import TextInjector from '@/components/TextInjector.vue'
import axios from 'axios'

const navigationStore = useNavigationStore()
const chapterStore = useChapterStore()

onMounted(async () => {
  navigationStore.showTopNav = true
  
})

const chapter = await getCurrentChapter(navigationStore.chapterNumber)

async function getCurrentChapter (chapterNumber) {
  if (chapterStore.dataLoaded === false) {
    await axios
      .get(`/api/v1/chapter/${chapterNumber}/`)
      .then(response => {
        chapterStore.processChapter(response.data[0])
        document.title = 'Book | ' + chapterStore.chapter.name
        console.log('Current Chapter is: ', chapterStore.currentChapter)
        closestParagraphId.value = localStorage.getItem('closestParagraphId')
        console.log('Closest Paragraph: ', closestParagraphId.value)
        if (closestParagraphId.value) {
          const paragraph = document.getElementById(closestParagraphId.value)
          console.log(paragraph)
          if (paragraph) {
            console.log('Scrolling to: ', closestParagraphId.value)
            paragraph.scrollIntoView()
          }
        }
        if (localStorage.getItem('dataLoaded')) {
          if (localStorage.getItem('savedScrollPosition') > 0) {
            scrollTo()
          }
        }

      })
      .catch(error => {
        console.log(error)
      })
  }
}

onActivated(() => {
  if (localStorage.getItem('dataLoaded')) {
    if(localStorage.getItem('savedScrollPosition') > 0) {
      scrollTo()
    }
  }
})

function scrollTo () {
  const paragraph = localStorage.getItem('savedScrollPosition')
  const element = document.getElementById(paragraph)
  const rect = element.getBoundingClientRect()
  console.log('Trying to scroll to paragraph:', paragraph)
  window.scrollTo({
    left: rect.left + window.scrollX, 
    top: rect.top + window.scrollY, 
    behavior: 'instant'
  })
  navigationStore.hideTopNav()
}

</script>
