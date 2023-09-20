import { defineStore } from 'pinia'

export const useNavigationStore = defineStore('nav', {
  state: () => ({
    lastScrollPosition: 0,
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
    }
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
    calcTotal (stat) {
      return Math.floor(stat.base + stat.increased + Math.floor(parseFloat(stat.trained)))
    },
    hideTopNav () {
      this.showTopNav = false
    },
    toggleTopNav () {
      this.showTopNav = true
    },
    hideBackButton () {
      this.showBackButton = false
      this.showResBars = true
    },
    toggleBackButton () {
      this.showBackButton = true
      this.showResBars = false
    },
    hpTrue () {
      this.bars[0].show = true
    },
    hpFalse () {
      this.bars[0].show = false
    },
    apTrue () {
      this.bars[1].show = true
    },
    apFalse () {
      this.bars[1].show = false
    },
    mpTrue () {
      this.bars[2].show = true
    },
    mpFalse () {
      this.bars[2].show = false
    },
    stTrue () {
      this.bars[3].show = true
    },
    stFalse () {
      this.bars[3].show = false
    }
  },
  getters: {
    oddOrEven: (state) => {
      if (state.count % 2 === 0) return 'even'
      return 'odd'
    }
  }
})
