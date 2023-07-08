import { defineStore } from 'pinia'

export const useChapterStore = defineStore('chapter', {
  state: () => ({
    currentChapter: 1,
    currentEvent: 0,
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
    currentPlayer: Object,
    currentStats: Object,
    currentSkills: Object,
    currentQuests: Object,
    currentAchievements: Object,
    currentPact: Object,
    currentParagon: Object,
    currentInventory: [],
    currentEquipment: {
      head: Object,
      neck: Object,
      shoulders: Object,
      back: Object,
      chest: Object,
      wrist: Object,
      waist: Object,
      underpants: Object,
      legs: Object,
      feet: Object,
      hands: [],
      ranged: Object,
      trinket: Object,
      rings: [],
      earrings: []
    }
  }),
  actions: {
    changeChapter (number) {
      this.currentChapter = number
    }
  },
  getters: {
    kaleOrAnna: (state) => {
      if (state.currentChapter % 4 === 0) return 'Anna'
      return 'Kale'
    },
    getChapter: (state) => {
      return state.chapter
    }
  }
})
