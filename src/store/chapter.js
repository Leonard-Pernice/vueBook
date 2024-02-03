import { defineStore } from 'pinia'
import { useNavigationStore } from '.'

export const useChapterStore = defineStore('chapter', {
  state: () => ({
    currentChapter: 0,
    currentEvent: 0,
    dataLoaded: false,
    initialized: false,
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
    processChapter (chapter) {
      try {
        this.loading = true
        const entries = chapter
        const numericKey = /^\d+$/
        const { data, paragraphs } = Object.keys(entries).reduce((acc, key) => {
          if (numericKey.test(key)) {
            acc.paragraphs[key] = entries[key]
          } else {
            acc.data[key] = entries[key]
          }
          return acc
        },
        { data: {}, paragraphs: {} })
        this.chapter = this.copySurfaceData(data)
        this.segregateStores(data)
        this.paragraphs = paragraphs
        this.currentChapter = this.chapter.name.replace(/[^0-9]/g, '')
        console.log('Current Chapter is: ', this.currentChapter)
        this.assumeInitialState()
      } catch (error) {
        console.error(error)
      } finally {
        this.loading = false
        this.dataLoaded = true
        localStorage.setItem('dataLoaded', this.dataLoaded)
      }
    },
    copySurfaceData (data) {
      const copy = {}
      for (const key in data) {
        const value = data[key]
        if (value !== null && typeof value === 'object') {
          continue
        }
        copy[key] = data[key]
      }
      return copy
    },
    segregateStores (obj) {
      // Characters
      this.characters = {}
      this.characters = this.insertSurfaceData(obj, 'characters')
      // Players
      this.players = {}
      this.players = this.insertDeepData(obj['characters'], 'players')
      // Stats
      this.stats = {}
      this.stats = this.insertDeepData(this.players, 'stats')
      // Skills
      this.skills = {}
      this.skills = this.insertDeepData(this.players, 'skills')
      // Items
      this.items = {}
      this.items = this.insertDeepData(obj['characters'], 'items')
      // Relationships
      this.relationships = {}
      this.relationships = this.insertDeepData(this.players, 'relationships')
      // Achievements
      this.achievements = {}
      this.achievements = this.insertDeepData(this.players, 'achievements')
      // Quests
      this.quests = {}
      this.quests = this.insertDeepData(this.players, 'quests')
      // // Inventories
      // this.inventories = {}
      // this.inventories = this.insertDeepData(this.players, 'inventories')
      // // Slots
      // this.slots = {}
      // this.slots = this.insertDeepData(this.inventories, 'slots')
      // // Equipments
      // this.equipments = {}
      // this.equipments = this.insertDeepData(this.players, 'equipments')
      // Currencies
      this.currencies = {}
      this.currencies = this.insertDeepData(this.players, 'currencies')
    },
    insertSurfaceData (obj, key) {
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
    },
    insertDeepData (obj, key) {
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
      while (!this.dataLoaded) {
        await new Promise(resolve => setTimeout(resolve, 100))
      }
      // INITIALIZE
      console.log('INITIALIZING!')
      const keys = Object.keys(this.players)
      this.currentPlayer = this.players[keys[0]]
      this.currentCharacter = this.getCharacter(this.currentPlayer.character.id)
      // console.log(this.currentCharacter)
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
      this.initialized = true
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
      const keys = Object.keys(this.characters)
      for (let i = 0; i < keys.length; i++) {
        const character = this.characters[keys[i]]
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
