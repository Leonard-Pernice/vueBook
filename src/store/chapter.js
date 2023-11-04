import { defineStore } from 'pinia'
import { useNavigationStore } from '.'

export const useChapterStore = defineStore('chapter', {
  state: () => ({
    currentChapter: 1,
    currentEvent: 0,
    dataLoaded: false,
    chapter: Object,
    paragraphs: Object,
    eventParagraphs: Object,
    characters: Object,
    players: Object,
    stats: Object,
    skills: Object,
    relationships: Object,
    achievements: Object,
    quests: Object,
    pacts: Object,
    paragons: Object,
    inventories: Object,
    slots: Object,
    equipments: Object,
    items: Object,
    currencies: Object,
    currentCharacter: Object,
    currentPlayer: Object,
    // currentStats: [],
    // currentSkills: [],
    // currentQuests: [],
    // currentAchievements: [],
    // currentPact: [],
    // currentParagon: [],
    // currentInventory: [],
    // currentEquipment: [],
    current: {
      stats: [],
      skills: [],
      quests: [],
      achievements: [],
      pacts: [],
      paragons: [],
      inventories: [],
      equipments: []
    }
  }),
  actions: {
    async fetchData() {
      let counter = 0
      while (this.stats.length <= 1) {
        await new Promise((resolve) => setTimeout(resolve, 100))
        counter += 1
        if (counter > 10) {
          break
        }
        console.log('Waiting...')
      }
      if (Object.keys(this.stats).length > 1) {
        this.dataLoaded = true;
        console.log('done waiting.')
      }
    },
    changeChapter (number) {
      this.currentChapter = number
    },
    getCorrespondingObject (key) {
      for (const mainKey in this) {
        if (key === mainKey) {
          return mainKey
        }
      }
      return null
    },
    getNavStore () {
      const navigationStore = useNavigationStore()
      return navigationStore
    },
    async assumeInitialState () {
      // Wait until data is loaded
      this.fetchData()
      while (!this.dataLoaded) {
        await new Promise(resolve => setTimeout(resolve, 100));
      }
      // INITIALIZE
      console.log('INITIALIZING!')
      const keys = Object.keys(this.players)
      this.currentPlayer = this.players[keys[0]]
      this.currentCharacter = this.getCharacter(this.currentPlayer.character)
      const firstParagraph = this.paragraphs[this.getLowestNumberedParagraph()].id
      for (const category in this.current) {
        const corresponding = this.getCorrespondingObject(category)
        this.current[category] = []
        for (const key in this[corresponding]) {
          const newEvent = this[corresponding][key]
          if (newEvent.referenceParagraph === firstParagraph) {
            this.current[category].push(newEvent)
          }
        }
      }
      for (const stat of this.current.stats) {
        const navigationStore = this.getNavStore()
        navigationStore.showStat(stat)
      }
    },
    getLowestNumberedParagraph () {
      const keys = Object.keys(this.paragraphs)
      let minNum = Infinity
      let minKey = ""
  
      keys.forEach(key => {
          let num = parseInt(key.split("_")[0])
          if (num < minNum) {
              minNum = num
              minKey = key
          }
      })
  
      return minKey
    },
    getCharacter (id) {
      for (const character in this.characters) {
        if (character.id === id) {
          return character
        }
      }
      return null
    }
  },
  getters: {
    kaleOrAnna: (state) => {
      if (state.currentChapter % 4 === 0) return 'Anna'
      return 'Kale'
    },
    getChapter: (state) => {
      return state.chapter
    },
    getStateObject: (state) => {
      return state
    }
  }
})
