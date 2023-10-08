export function findEvent (obj, id) {
  let ret
  for (const key in obj) {
    if (key.includes(id)) {
      ret = obj[key]
    }
  }
  return ret
}

export function findPlayer (obj, id) {
  let ret
  for (const key in obj) {
    if (obj[key].id === id) {
      ret = obj[key]
    }
  }
  return ret
}

export function calcExp (msg) {
  const lvl = parseInt(msg.level)
  const power = parseInt(msg.difficulty)
  const tier = parseInt(msg.tier)
  const typ = msg.type
  const base = 1.00
  let reward
  if (msg.statusOfQuest === 'Completed') {
    return parseFloat(msg.exp_received).toFixed(2)
  }
  if (typ === 'achievement' || typ === 'quest') {
    if (lvl === 0) {
      return base
    }
    switch (tier) {
      case 0:
        if (lvl === 1) {
          reward = 0.125
          return reward
        }
        reward = base / 2 / Math.pow(lvl, 2)
        return (reward * 10000).toFixed(2)
      case 1: // power = difficulty!
        reward = base * base / 3 * Math.pow(power, 2) / Math.pow(lvl, 2) / 45 * lvl
        return (reward * 10000).toFixed(2)
      default:
        reward = base * base * Math.pow(power, 2) / Math.pow(lvl, 2)
        return (reward * 10000).toFixed(2)
    }
  } else {
    return 0.00
  }
}

// export function calcStatValue (stat) {
//   return (stat[1] === 0 ? ('-') : ((stat[1] === stat[3]) ? ('') : (stat[3] / (stat[1]) * 100).toFixed(0) + '%'))
// }

// export function calcMaxStat (stat, s) {
//   return ((stat[4] === 0) ? ('white') : (stat[1] / stat[4] >= (s / 10)) ? ('white') : ('transparent'))
// }

export function calcStatPointsOnLevel(lvl) {
  const statpoints = Math.round(lvl + Math.pow(Math.floor(lvl / 10), Math.log(lvl * 2)))
  return statpoints;
}

export function calcAccumulatedStatPoints(lvl) {
  const level = Math.floor(lvl)
  let total = 0;
  if (level == 1) {
      return 1;
  } else if(level == 0) {
      return 0;
  } else {
      total += calcStatPointsOnLevel(level) + calcAccumulatedStatPoints(level - 1)
      return total;
  }
}

export const statAbreviations = {
  vit: 'Vitality',
  str: 'Strength',
  agi: 'Agility',
  sp: 'Spirit',
  mom: 'Momentum',
  cha: 'Charisma',
  con: 'Constitution',
  foc: 'Focus',
  end: 'Endurance',
  per: 'Perception',
  spd: 'Speed',
  acc: 'Accuracy',
  eva: 'Evasion',
  stam: 'Stamina',
  intimidation: 'Intimidation',
  control: 'Control',
  eleminsight: 'Elemental Insight',
  magicres: 'Magic Resistance',
  physres: 'Physical Resistance',
  mentalres: 'Mental Resistance',
  mig: 'Might',
  sen: 'Sense',
  log: 'Logic',
  int: 'Intuition',
  wil: 'Willpower',
  atr: 'Attractiveness'
  // Cognisance, aptitude, conductance, capacity, fluidity (of mana through body)
}
