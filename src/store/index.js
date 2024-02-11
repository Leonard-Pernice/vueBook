import { defineStore } from 'pinia'

export const useNavigationStore = defineStore('nav', {
  state: () => ({
    activePage: '',
    chapterNumber: 1,
    lastScrollPosition: 0,
    savedScrollPosition: 0,
    eventParagraphHeights: {},
    paragraphHeights: {},
    showTopNav: true,
    showBackButton: false,
    showResBars: true,
    showChapterNav: false,
    bars: {
      'Vitality': false,
      'Momentum': false,
      'Charisma': false,
      'Spirit': false
    },
    storyDropDown: {}
  }),
  actions: {
    showStat (stat) {
      const validBars = ['Vitality', 'Momentum', 'Charisma', 'Spirit']
      if (validBars.includes(stat.name) && this.calcTotal(stat) > 0) {
        this.bars[stat.name] = true
      } else {
        this.bars[stat.name] = false
      }
    },
    changeActivePage () {
      const page = window.location.pathname.split('/')[1]
      this.activePage = page
      const menus = ['character', 'skills', 'quests', 'achievements', 'pacts', 'paragons']
      if (menus.includes(page)) {
        this.showResBars = false
      } else {
        this.showResBars = true
      }
    },
    calcTotal (stat) {
      return Math.floor(stat.base + stat.increased + Math.floor(parseFloat(stat.trained)))
    },
    hideTopNav () { this.showTopNav = false },
    toggleTopNav () { this.showTopNav = true },
    hideBackButton () {
      this.showBackButton = false
      this.showResBars = true
      this.hideTopNav()
    },
    toggleBackButton () {
      this.showBackButton = true
      this.showResBars = false
    },
    hideResBars() {
      this.showResBars = false
    },
    toggleResBars() {
      this.showResBars = true
    },
    hpTrue () { this.bars[0].show = true },
    hpFalse () { this.bars[0].show = false },
    apTrue () { this.bars[1].show = true },
    apFalse () { this.bars[1].show = false },
    mpTrue () { this.bars[2].show = true },
    mpFalse () { this.bars[2].show = false },
    stTrue () { this.bars[3].show = true },
    stFalse () { this.bars[3].show = false }
  },
  getters: {
    oddOrEven: (state) => {
      if (state.count % 2 === 0) return 'even'
      return 'odd'
    }
  }
})
