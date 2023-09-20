<template>
  <div class="w-screen h-screen">
    <div class="flex-col justify-center items-center pt-20">
      <h1 class="text-white text-5xl text-center">My Account</h1>
      <hr>
      <div class="flex justify-center items-center my-10">
        <div class="w-96">
          <button @click="navigateToCurrentChapter()" class="bg-green-400 hover:bg-green-500 text-white py-2 px-4 rounded-md w-full">Go back to current chapter: {{ chapterStore.currentChapter }}</button>
        </div>
      </div>
      <hr>
      <div class="flex justify-center items-center my-10">
        <div class="border border-white w-96 h-24 p-2">
          <!-- <input type="number" id="chapterNumber" value="0"> -->
          <input type="file" id="jsonChapterFile" @change="loadJson()" />
          <button @click="createChapter()" class="bg-green-400 hover:bg-green-500 text-white py-2 px-4 rounded-md w-full">Log Entries</button>
        </div>
      </div>
      <div class="flex justify-center items-center my-10">
        <div class="w-96 p-2">
          <!-- <input type="number" id="chapterNumber" value="0"> -->
          <button @click="logout()" class="w-full mb-4 bg-red-500 hover:bg-red-700 text-white py-2 px-4 rounded-md">Log out</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useChapterStore } from '@/store/chapter'
import { useAccountStore } from '@/store/account'
import axios from 'axios'
import { useRouter, useRoute } from 'vue-router'
import { ref } from 'vue'
// import  CircleProgressBar from 'vue3-m-circle-progress-bar'
// import 'vue3-m-circle-progress-bar/style.css'

const chapterStore = useChapterStore()
const accountStore = useAccountStore()

const router = useRouter()
const route = useRoute()

const entries = ref([])
const chapterNumber = ref()
const chapter = ref()
const stats = ref({
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
})
// const existingChapters = ref([])

async function parseJsonFile () {
  const fileInput = document.getElementById('jsonChapterFile')
  const file = fileInput.files[0]
  // Extract the number from the chapter file name
  const match = file.name.match(/(\d+)/)
  chapterNumber.value = match ? parseInt(match[1]) : 0
  console.log('The current chapter being processed is Chapter:', chapterNumber.value)
  // const file = event.target.files[0]
  return new Promise((resolve, reject) => {
    const fileReader = new FileReader()
    fileReader.onload = event => resolve(JSON.parse(event.target.result))
    fileReader.onerror = error => reject(error)
    fileReader.readAsText(file)
  })
}

async function loadJson () {
  entries.value = await parseJsonFile()
}

const logEntries = async (index = 0) => {
  if (index >= entries.value.content.length) {
    console.log('All entries posted.')
    return
  }
  try {
    const text = entries.value.content[index][1]
    const options = entries.value.content[index][0]
    let formData
    switch (options.class) {
      case 'killmsg':
        formData = {}
        createKillEventParagraph(formData, index)
        break
      case 'apUsed':
      case 'mpUsed':
      case 'stUsed':
        formData = {
          chapter: chapter.value,
          text: '',
          attributes: options.class,
          textorder: index + 0.1
        }
        createSkillUsedParagraph(formData, index)
        break
      case 'statSpent':
        formData = {
          chapter: chapter.value,
          text: '',
          attributes: options.class,
          textorder: index + 0.15
        }
        createStatUpdateParagraph(formData, index)
        break
      case 'dmgtaken':
        formData = {
          chapter: chapter.value,
          text: '',
          attributes: options.class,
          textorder: index + 0.35
        }
        createDamageUpdateParagraph(formData, index)
        break
      case 'stim':
        formData = {
          chapter: chapter.value,
          text: '',
          attributes: options.class,
          textorder: index + 0.30
        }
        createDamageUpdateParagraph(formData, index)
        break
      case 'characterInitialization':
        formData = {
          chapter: chapter.value,
          text: '',
          attributes: 'character',
          textorder: index + 0.70
        }
        initializeCharacter(formData, index)
        break
      case 'playerInitialization':
        formData = {
          chapter: chapter.value,
          text: '',
          attributes: 'player',
          textorder: index + 0.60
        }
        initializePlayer(formData, index)
        break
      case 'statUnlocked':
        formData = {
          chapter: chapter.value,
          text: '',
          attributes: 'stat',
          textorder: index + 0.65
        }
        initializeStat(formData, index)
        break
      case 'skillUnlocked':
        formData = {
          chapter: chapter.value,
          text: '',
          attributes: 'skill',
          textorder: index + 0.66
        }
        initializeSkill(formData, index)
        break
      case 'relationshipInitialization':
        formData = {
          chapter: chapter.value,
          text: '',
          attributes: 'relationship',
          textorder: index + 0.71
        }
        initializeRelationship(formData, index)
        break
      case 'questUnlocked':
        formData = {
          chapter: chapter.value,
          text: options.name,
          attributes: 'quest',
          textorder: index + 0.61
        }
        initializeQuest(formData, index)
        break
      case 'itemInitialization':
        formData = {
          chapter: chapter.value,
          text: '',
          attributes: 'item',
          textorder: index + 0.81
        }
        initializeItem(formData, index)
        break
      // case 'inventoryInitialization':
      //   formData = {
      //     chapter: chapter.value,
      //     text: '',
      //     attributes: 'inventory',
      //     textorder: index + 0.63
      //   }
      //   initializeInventory(formData, index)
      //   break
      // case 'slotInitialization':
      //   formData = {
      //     chapter: chapter.value,
      //     text: '',
      //     attributes: 'slot',
      //     textorder: index + 0.635
      //   }
      //   initializeSlot(formData, index)
      //   break
      // case 'equipmentInitialization':
      //   formData = {
      //     chapter: chapter.value,
      //     text: '',
      //     attributes: 'equipment',
      //     textorder: index + 0.635
      //   }
      //   initializeEquipment(formData, index)
      //   break
      default:
        formData = {
          chapter: chapter.value,
          text: text,
          textorder: index + 0.0
        }
        createTextParagraph(formData, index)
    }
  } catch (error) {
    console.error(`Error posting entry ${index}: ${error.message}`)
  }
}

// async function getAllChapters () {
//   await axios
//     .get('/api/v1/create-chapter/1/')
//     .then(response => {
//       existingChapters.value = response.data
//     })
//     .catch(error => {
//       console.log(JSON.stringify(error))
//     })
// }

async function createChapter () {
  chapter.value = 'Chapter ' + chapterNumber.value
  await axios.get('api/v1/get-book/1/').then(response => {
    const formData = {
      book: parseInt(response.data.id),
      name: chapter.value
    }
    console.log(formData)
    axios.get('api/v1/get-chapter/', {
      params: { name: chapter.value }
    }).then(response => {
      console.log('Chapter exists already. Now posting paragraphs...')
      chapter.value = response.data.id
      logEntries()
    }).catch(error => {
      console.log(error, 'Chapter does not exist. Now creating...')
      axios
        .post('api/v1/chapters/', formData)
        .then(response => {
          console.log('Chapter created. Now posting paragraphs...')
          chapter.value = response.data.id
          logEntries()
        }).catch(error => { console.log(error) })
    })
  }).catch(error => { console.log(error) })
}

function createTextParagraph (formData, index) {
  axios
    .post('api/v1/create-paragraph/', formData)
    .then(response => {
      console.log(`Posted entry ${response.data}. Now posting ${index + 1}`)
      logEntries(index + 1)
    }).catch(error => { console.log(error) })
}

function createKillEventParagraph (formData, index) {
  const text = entries.value.content[index][1]
  const options = entries.value.content[index][0]
  if (options.power) {
    options.power = options.power.replace(/[^0-9]/g, '')
  }
  if (options.difficulty) {
    options.difficulty = options.difficulty.replace(/[^0-9]/g, '')
  }
  options.tier = options.tier.replace(/[^0-9]/g, '')
  console.log(`Processing a kill paragraph for a ${options.type}.`)
  const playerName = options.character ? options.character : 'Kale' // not to be confused with the
  // normal Character name value in the options object... here I'm asking for the player's name,
  // since only players will  ever have stats.
  console.log('Retrieving all player objects in chapter id ', chapter.value)
  axios.get('api/v1/create-player/', {
    params: {
      chapter: chapter.value,
      index: index,
      name: playerName
    }
  }).then(response => {
    const lastPlayerReference = response.data.reduce((prev, current) => { // taking the most recently posted player instance
      return prev.id > current.id ? prev : current
    })
    options.level = lastPlayerReference.level
    const expFromEvent = parseFloat(calcExp(options))
    const calculatedLevel = Math.floor(lastPlayerReference.level + parseFloat(lastPlayerReference.exp) + expFromEvent)
    const calculatedExp = parseFloat(lastPlayerReference.exp) + expFromEvent - Math.floor(parseFloat(lastPlayerReference.exp) + expFromEvent)
    console.log(lastPlayerReference)
    console.log('Reference level: ', lastPlayerReference.level)
    console.log('Reference EXP: ', parseFloat(lastPlayerReference.exp))
    console.log('Exp from event: ', expFromEvent)
    console.log(`Calculated level: ${calculatedLevel}`)
    console.log(`Calculated EXP: ${calculatedExp.toFixed(4)}`)
    const killEventFormData = {
      chapter: chapter.value,
      text: options.content,
      textorder: index + 0.5,
      attributes: options.type,
      exp: expFromEvent.toFixed(4)
    }
    console.log(lastPlayerReference)
    axios
      .post('api/v1/create-eventparagraph/', killEventFormData)
      .then(response => {
        const killParagraph = response.data.id
        const playerFormData = {
          character: lastPlayerReference.character,
          name: playerName,
          referenceParagraph: killParagraph,
          referenceToLastRelevantEvent: lastPlayerReference.id,
          characterName: lastPlayerReference.characterName,
          job: lastPlayerReference.job,
          title: lastPlayerReference.title,
          level: calculatedLevel,
          exp: calculatedExp.toFixed(4),
          typ: lastPlayerReference.typ
        }
        console.log('Trying to update player object:', playerFormData)
        axios.post('api/v1/create-player/', playerFormData).then(response => {
          console.log(`Posted new Player object with changed exp and maybe level available at index: ${index + 0.15}`)
          const newPlayer = response.data
          if (options.type === 'achievement') {
            const achievementFormData = {
              player: newPlayer.id,
              name: options.name,
              referenceParagraph: killParagraph,
              referenceToLastRelevantEvent: lastPlayerReference.id, // This is an unnecessary field...
              description: options.description,
              tier: options.tier,
              difficulty: options.difficulty,
              reward: options.reward
            }
            console.log('Trying to post a new achievement.')
            axios.post('api/v1/create-achievement/', achievementFormData).then(response => {
              console.log(`Posted new achievement: ${response.data} at ${index + 0.5}`)
            }).catch(error => { console.log(error) })
          } else if (options.type === 'quest') {
            console.log('Retrieving the relevant quest object.')
            console.log(options)
            axios.get('api/v1/create-quest/', {
              params: {
                chapter: chapter.value,
                paragraph: killParagraph,
                playerName: lastPlayerReference.name,
                questName: options.content
              }
            }).then(response => {
              const lastQuestReference = response.data
              const newStatus = 'Completed'
              console.log(lastQuestReference)
              const questFormData = {
                player: newPlayer.id,
                name: options.content,
                referenceParagraph: killParagraph,
                referenceToLastRelevantEvent: lastQuestReference.id,
                statusOfQuest: newStatus,
                description: lastQuestReference.description,
                optional_description: lastQuestReference.optional_description,
                tier: lastQuestReference.tier,
                difficulty: lastQuestReference.difficulty,
                reward_title: lastQuestReference.reward_title,
                reward: lastQuestReference.reward,
                optional_reward: lastQuestReference.optional_reward,
                exp_received: (expFromEvent * 10000).toFixed(2)
              }
              console.log('QuestformData: ', questFormData)
              console.log('Trying to update the quest.')
              axios.post('api/v1/create-quest/', questFormData).then(response => {
                console.log(`Updated quest completion of quest ${response.data} at index: ${index + 0.5}.`)
              }).catch(error => { console.log(error) })
            })
          }
          if (!text === '') { // in case there is a paragraph connected to the kill
            const formDataAdditional = {
              chapter: chapter.value,
              text: text,
              textorder: index + 0.0
            }
            console.log('Posting an additional paragraph.')
            axios.post('api/v1/create-paragraph/', formDataAdditional).then(response => {
              console.log(`Posted killmsg ${response.data} ${index + 0.5} and additional entry ${index + 0.0}.`)
            }).catch(error => { console.log(error) })
          }
          if (calculatedLevel > lastPlayerReference.level && lastPlayerReference.name === 'Kale') {
            const levelUpFormData = {
              chapter: chapter.value,
              text: returnReward(calculatedLevel),
              textorder: index + 0.25,
              attributes: 'levelup',
              exp: newPlayer.level
            }
            console.log('Posting a levelup event paragraph.')
            axios.post('api/v1/create-eventparagraph/', levelUpFormData).then(response => {
              console.log(`Posted levelup event ${response.data} at index: ${index + 0.25}. Now continuing with index: ${index + 1}`)
              logEntries(index + 1)
            }).catch(error => { console.log(error) })
          } else {
            console.log(`No levelup here. Now continuing with index: ${index + 1}`)
            logEntries(index + 1)
          }
        }).catch(error => { console.log(error) })
      }).catch(error => { console.log(error) })
  }).catch(error => { console.log(error) })
}

function createSkillUsedParagraph (formData, index) {
  const text = entries.value.content[index][1]
  const options = entries.value.content[index][0]
  console.log('Posting a Skill Used event paragraph.')
  axios.post('api/v1/create-eventparagraph/', formData).then(response => {
    const referenceParagraph = response.data.id
    if (!text === '') {
      const formDataAdditional = {
        chapter: chapter.value,
        text: text,
        textorder: index + 0.0
      }
      console.log('Posting an additional paragraph.')
      axios.post('api/v1/create-paragraph/', formDataAdditional).then(response => {
        console.log(`Posted Skill used event ${response.data} at ${index + 0.1} and additional entry ${index + 0.0}.`)
      }).catch(error => { console.log(error) })
    }
    const skillName = capitalizeString(options.skill)
    const playerName = options.character ? options.character : 'Kale' // not to be confused with the
    // normal Character name value in the options object... here I'm asking for the player's name,
    // since only players will  ever have stats.
    console.log('Retrieving player objects in the chapter.')
    axios.get('api/v1/create-player/', {
      params: {
        chapter: chapter.value,
        paragraph: referenceParagraph,
        name: playerName
      }
    }).then(response => {
      const lastPlayerReference = response.data
      console.log(`Retrieving all ${skillName} skill entries of ${playerName}.`)
      axios.get('api/v1/create-skill/', {
        params: {
          chapter: chapter.value,
          playerName: playerName,
          skillName: skillName
        }
      }).then(response => {
        console.log(response.data)
        const lastSkillReference = response.data.reduce((prev, current) => { // taking the most recently posted skill instance
          return prev.id > current.id ? prev : current
        })
        const nameOfStatRelatedToCostOfSkill = options.ap ? 'Momentum' : options.mp ? 'Spirit' : options.st ? 'Charisma' : null
        console.log('Finding the cost related to ', skillName)
        axios.get('api/v1/create-stat/', {
          params: {
            route: 'statByName',
            chapter: chapter.value,
            paragraph: referenceParagraph,
            statName: nameOfStatRelatedToCostOfSkill,
            playerName: playerName
          }
        }).then(response => {
          const statRelatedToCostOfSkill = response.data
          const updatedSkillLevelAndExp = calcProgressExp(lastSkillReference.level + parseFloat(lastSkillReference.exp), findCost(options), statRelatedToCostOfSkill)
          const updatedSkillLevel = parseInt(Math.floor(updatedSkillLevelAndExp))
          const updatedSkillExp = parseFloat(updatedSkillLevelAndExp - Math.floor(updatedSkillLevelAndExp)).toFixed(4)
          console.log('Relevant Stat: ', statRelatedToCostOfSkill)
          console.log('Calculated exp gain: ', updatedSkillLevelAndExp)
          console.log('Cost: ', findCost(options))
          console.log('Calculated Skill level is: ', updatedSkillLevel)
          console.log('Reference level is: ', lastSkillReference.level)
          console.log('Reference exp is: ', lastSkillReference.exp)
          const formDataSkill = {
            player: lastPlayerReference.id,
            modifier: lastSkillReference.modifier,
            name: skillName,
            referenceParagraph: referenceParagraph,
            referenceToLastRelevantEvent: lastSkillReference.id,
            level: updatedSkillLevel,
            exp: updatedSkillExp,
            description: lastSkillReference.description,
            typ: lastSkillReference.typ,
            ap: lastSkillReference.ap,
            mp: lastSkillReference.mp,
            st: lastSkillReference.st
          }
          console.log(formDataSkill)
          console.log(`Updating ${skillName}.`)
          axios.post('api/v1/create-skill/', formDataSkill).then(response => {
            console.log('Posted Skill. Now posting the related Stat change.')
            const postedSkill = response.data
            console.log(`Retrieving stat modifier related to ${skillName}.`)
            axios.get('api/v1/create-stat/', {
              params: {
                route: 'statByID',
                chapter: chapter.value,
                statid: postedSkill.modifier,
                paragraph: referenceParagraph,
                playerName: lastPlayerReference.name
              }
            }).then(response => {
              const lastReferenceOfStat = response.data.reduce((prev, current) => { // taking the most recently posted stat instance
                return prev.id > current.id ? prev : current
              })
              const modifierStatLevel = parseInt(lastReferenceOfStat.base) + parseInt(lastReferenceOfStat.increased) + parseFloat(lastReferenceOfStat.trained)
              const modifierExpFromSkillUsed = calcProgressExp(modifierStatLevel, findCost(options), lastReferenceOfStat) - parseInt(lastReferenceOfStat.base) - parseInt(lastReferenceOfStat.increased)
              console.log(`Updated ${lastReferenceOfStat.name} as modifier of ${skillName}.`)
              const formDataStat = {
                player: postedSkill.player,
                name: lastReferenceOfStat.name,
                referenceParagraph: referenceParagraph,
                referenceToLastRelevantEvent: lastReferenceOfStat.id,
                base: lastReferenceOfStat.base,
                increased: lastReferenceOfStat.increased,
                trained: modifierExpFromSkillUsed.toFixed(2),
                bar: lastReferenceOfStat.bar
              }
              console.log(`Updating modifier of ${skillName}: ${lastReferenceOfStat.name}`)
              axios.post('api/v1/create-stat/', formDataStat).then(response => {
                console.log(response.data)
                console.log(statRelatedToCostOfSkill)
                console.log(options)
                console.log('Cost is: ', findCost(options))
                const costStatLevel = parseInt(statRelatedToCostOfSkill.base) + parseInt(statRelatedToCostOfSkill.increased) + parseFloat(statRelatedToCostOfSkill.trained)
                const costStatExpFromSkillUsed = calcProgressExp(costStatLevel, findCost(options), statRelatedToCostOfSkill) - parseInt(statRelatedToCostOfSkill.base) - parseInt(statRelatedToCostOfSkill.increased)
                const costFormData = {
                  player: postedSkill.player,
                  name: statRelatedToCostOfSkill.name,
                  referenceParagraph: referenceParagraph,
                  referenceToLastRelevantEvent: statRelatedToCostOfSkill.id,
                  base: statRelatedToCostOfSkill.base,
                  increased: statRelatedToCostOfSkill.increased,
                  trained: costStatExpFromSkillUsed.toFixed(2),
                  bar: statRelatedToCostOfSkill.bar + parseInt(findCost(options))
                }
                console.log(costFormData)
                console.log('previous trained: ', statRelatedToCostOfSkill.trained)
                console.log('calced trained: ', Math.ceil(formDataSkill.exp / 10))
                console.log('total calced: ', Math.floor((statRelatedToCostOfSkill.trained + Math.ceil(formDataSkill.exp / 10)) * 100) / 100)
                console.log('Posting the updated stat with the cost of ', skillName)
                axios.post('api/v1/create-stat/', costFormData).then(response => {
                  console.log(`Updated ${nameOfStatRelatedToCostOfSkill} in ${response.data} with the cost of ${postedSkill}.`)
                  logEntries(index + 1)
                }).catch(error => { console.log(error) })
              }).catch(error => { console.log(error) })
            }).catch(error => { console.log(error) })
          }).catch(error => { console.log(error) })
        }).catch(error => { console.log(error) })
      }).catch(error => { console.log(error) })
    }).catch(error => { console.log(error) })
  }).catch(error => { console.log(error) })
}

function createStatUpdateParagraph (formData, index) {
  const text = entries.value.content[index][1]
  const options = entries.value.content[index][0]
  console.log('Posting a stat update paragraph (stat point(s) spent).')
  axios.post('api/v1/create-eventparagraph/', formData).then(response => {
    console.log(`Posted Stat Update Reference Paragraph at Index: ${index + 0.15}.`)
    const referenceParagraph = response.data.id
    const playerName = options.character ? options.character : 'Kale' // not to be confused with the
    // normal Character name value in the options object... here I'm asking for the player's name,
    // since only players will  ever have stats.
    console.log('Retrieving all stats related to player in the chapter.')
    axios.get('api/v1/create-stat/', {
      params: {
        route: 'allStatsOfPlayer',
        chapter: chapter.value,
        paragraph: referenceParagraph,
        playerName: playerName
      }
    }).then(response => {
      const allStatsOfPlayer = response.data
      for (const statShorthand in stats) {
        if (options[statShorthand] > 0 || options[stats[statShorthand]] > 0) {
          // eslint-disable-next-line no-unused-vars
          const lastRelevantStat = Object.fromEntries(Object.entries(allStatsOfPlayer).filter(([key, value]) => value.name === stats[statShorthand])).reduce((prev, current) => { // taking the most recently posted stat instance with that name
            return prev.id > current.id ? prev : current
          })
          const statFormData = {
            player: lastRelevantStat.player,
            name: lastRelevantStat.name,
            referenceParagraph: referenceParagraph,
            referenceToLastRelevantEvent: lastRelevantStat.referenceParagraph,
            base: lastRelevantStat.base,
            increased: lastRelevantStat.increased + Math.max(Number(options[statShorthand]) || 0, Number(options[stats[statShorthand]]) || 0),
            trained: lastRelevantStat.trained,
            bar: lastRelevantStat.bar + Math.floor(Math.max(Number(options[statShorthand]) || 0, Number(options[stats[statShorthand]]) || 0))
          }
          console.log(`Looping over relevant stats. Now trying to post ${lastRelevantStat.name}`)
          axios.post('api/v1/create-stat/', statFormData).then(response => {
            const updatedStat = response.data
            console.log(`Updated ${updatedStat.name} related to index: ${index + 0.15}. Now updating the statpoints spent in the player object.`)
            // ----------------------------------------------------------------------------------------
            // decided FOR NOW that statPoints available will NOT be part of player objects in django
            // this means THE ONLY WAY to increase stat points will be via spending them after levelups
            // ----------------------------------------------------------------------------------------

            // axios.get('api/v1/create-player/', {
            //   chapter: chapter.value,
            //   name: playerName
            // }).then(response => {
            //   const lastPlayerReference = response.data.reduce((prev, current) => { // taking the most recently posted player instance
            //     return prev.id > current.id ? prev : current
            //   })
            //   const playerFormData = {
            //     character: lastPlayerReference.character,
            //     name: playerName,
            //     referenceParagraph: referenceParagraph,
            //     referenceToLastRelevantEvent: lastPlayerReference.referenceParagraph,
            //     characterName: lastPlayerReference.characterName,
            //     job: lastPlayerReference.job,
            //     title: lastPlayerReference.title,
            //     level: lastPlayerReference.level,
            //     exp: lastPlayerReference.exp,
            //     typ: lastPlayerReference.typ
            //   }
            //   axios.post('api/v1/create-player/', playerFormData).then(response => {
            //     console.log(`Posted new Player object with changed Statpoints available at index: ${index + 0.15}`)
            //   }).catch(error => { console.log(error) })
            // }).catch(error => { console.log(error) })
          }).catch(error => { console.log(error) })
        }
      }
      if (text !== '') {
        const additionalParagraphFormData = {
          chapter: chapter.value,
          text: text,
          textorder: index + 0.0
        }
        console.log('Posting an additional text paragraph.')
        axios.post('api/v1/create-paragraph/', additionalParagraphFormData).then(response => {
          console.log(`Posted additional paragraph ${response.data} at index: ${index + 0.0}. Now posting at ${index + 1}`)
          logEntries(index + 1)
        }).catch(error => { console.log(error) })
      } else {
        console.log(`Now posting at ${index + 1}`)
        logEntries(index + 1)
      }
    }).catch(error => { console.log(error) })
  }).catch(error => { console.log(error) })
}

function createDamageUpdateParagraph (formData, index) {
  const text = entries.value.content[index][1]
  const options = entries.value.content[index][0]
  options.dmg = options.dmg.replace(/[^0-9-]/g, '')
  console.log('Posting a damage taken event paragraph.')
  axios.post('api/v1/create-eventparagraph/', formData).then(response => {
    console.log(`Posted Stat Bar Update Reference Paragraph at Index: ${index + 0.15}.`)
    const referenceParagraph = response.data.id
    const playerName = options.character ? options.character : 'Kale' // not to be confused with the
    // normal Character name value in the options object... here I'm asking for the player's name,
    // since only players will  ever have stats.
    console.log('Retrieving the latest player instance of ', playerName)
    axios.get('api/v1/create-player/', {
      params: {
        chapter: chapter.value,
        name: playerName,
        paragraph: referenceParagraph
      }
    }).then(response => {
      const latestPlayerInstance = response.data
      const relevantStat = options.class === 'dmgtaken' ? 'Vitality' : 'Charisma'
      console.log(`Retrieving all ${relevantStat} instances in the chapter.`)
      axios.get('api/v1/create-stat/', {
        params: {
          route: 'statByName',
          chapter: chapter.value,
          statName: relevantStat,
          paragraph: referenceParagraph,
          playerName: playerName
        }
      }).then(response => {
        const lastRelevantStat = response.data
        // const lastRelevantStat = Object.values(Object.fromEntries(Object.entries(allStatsOfPlayer).filter(([key, value]) => value.name === relevantStat))).reduce((prev, current) => { // taking the most recently posted stat instance with that name
        //   return prev.id > current.id ? prev : current
        // })
        console.log('Bar of last relevant stat: ', lastRelevantStat.bar)
        console.log('+ damage in chapter:', options.dmg)
        console.log(latestPlayerInstance)
        const damagedStatLevel = parseInt(lastRelevantStat.base) + parseInt(lastRelevantStat.increased) + parseFloat(lastRelevantStat.trained)
        const damagedStatExp = calcProgressExp(damagedStatLevel, options.dmg, lastRelevantStat) - parseInt(lastRelevantStat.base) - parseInt(lastRelevantStat.increased)
        const statFormData = {
          player: latestPlayerInstance.id,
          name: lastRelevantStat.name,
          referenceParagraph: referenceParagraph,
          referenceToLastRelevantEvent: lastRelevantStat.referenceParagraph,
          base: lastRelevantStat.base,
          increased: lastRelevantStat.increased,
          trained: damagedStatExp.toFixed(2),
          bar: lastRelevantStat.bar + Math.floor(options.dmg)
        }
        console.log(`Updating ${relevantStat} to new bar value.`)
        console.log(statFormData)
        axios.post('api/v1/create-stat/', statFormData).then(response => {
          const updatedStat = response.data
          console.log(`Updated ${updatedStat.name}'s bar value, related to index: ${index + 0.15}.`)
        }).catch(error => { console.log(error) })
        if (text !== '') {
          const additionalParagraphFormData = {
            chapter: chapter.value,
            text: text,
            textorder: index + 0.0
          }
          console.log('Posting additional text paragraph.')
          axios.post('api/v1/create-paragraph/', additionalParagraphFormData).then(response => {
            console.log(`Posted additional paragraph ${response.data} at index: ${index + 0.0}. Now posting at ${index + 1}`)
            logEntries(index + 1)
          }).catch(error => { console.log(error) })
        } else {
          console.log(`Now posting at ${index + 1}`)
          logEntries(index + 1)
        }
      }).catch(error => { console.log(error) })
    }).catch(error => { console.log(error) })
  }).catch(error => { console.log(error) })
}

function initializeCharacter (formData, index) {
  const text = entries.value.content[index][1]
  const options = entries.value.content[index][0]
  console.log('Posting Character Creation event paragraph.')
  axios.post('api/v1/create-eventparagraph/', formData).then(response => {
    console.log(`Posted Character Creation Reference Paragraph at Index: ${index + 0.70}.`)
    const referenceParagraph = response.data.id
    const newCharacterFormData = {
      chapter: chapter.value,
      referenceParagraph: referenceParagraph,
      name: options.name,
      lastname: options.lastname,
      information: options.information,
      statusOfNpc: options.status,
      age: options.age,
      gender: options.gender,
      height: parseInt(options.height),
      weight: parseInt(options.weight),
      species: options.species,
      race: options.race
    }
    axios.post('api/v1/create-character/', newCharacterFormData).then(response => {
      const newCharacter = response.data
      console.log('Created ', newCharacter.name, ' ', newCharacter.lastname)
      if (text !== '') {
        const additionalParagraphFormData = {
          chapter: chapter.value,
          text: text,
          textorder: index + 0.0
        }
        console.log('Posting additional text paragraph.')
        axios.post('api/v1/create-paragraph/', additionalParagraphFormData).then(response => {
          console.log(`Posted additional paragraph ${response.data} at index: ${index + 0.0}. Now posting at ${index + 1}`)
          logEntries(index + 1)
        }).catch(error => { console.log(error) })
      } else {
        console.log(`Now posting at ${index + 1}`)
        logEntries(index + 1)
      }
    }).catch(error => { console.log(error) })
  }).catch(error => { console.log(error) })
}

function initializePlayer (formData, index) {
  const text = entries.value.content[index][1]
  const options = entries.value.content[index][0]
  console.log('Posting a Player Creation event paragraph.')
  axios.post('api/v1/create-eventparagraph/', formData).then(response => {
    console.log(`Posted Player Creation Reference Paragraph at Index: ${index + 0.60}.`)
    const referenceParagraph = response.data.id
    console.log('Retrieving all Characters in the chapter appearing before this paragraph...')
    axios.get('api/v1/create-character/', { params: { chapter: chapter.value, paragraph: referenceParagraph } }).then(response => {
      const characterList = response.data
      let relevantCharacter
      for (let i = 0; i < characterList.length; i++) {
        if (characterList[i].name + characterList[i].lastname === options.characterName) {
          relevantCharacter = characterList[i]
        }
      }
      if (relevantCharacter) {
        console.log('Creating the player instance: ', options.name)
        const newPlayerFormData = {
          character: relevantCharacter.id,
          name: options.name,
          referenceParagraph: referenceParagraph,
          characterName: options.characterName,
          job: options.job,
          title: options.title,
          level: options.level,
          exp: options.exp,
          typ: options.typ
        }
        axios.post('api/v1/create-player/', newPlayerFormData).then(response => {
          const newPlayer = response.data
          console.log('Created Player: ', newPlayer.name)
          if (text !== '') {
            const additionalParagraphFormData = {
              chapter: chapter.value,
              text: text,
              textorder: index + 0.0
            }
            console.log('Posting additional text paragraph.')
            axios.post('api/v1/create-paragraph/', additionalParagraphFormData).then(response => {
              console.log(`Posted additional paragraph ${response.data} at index: ${index + 0.0}. Now posting at ${index + 1}`)
              logEntries(index + 1)
            }).catch(error => { console.log(error) })
          } else {
            console.log(`Now posting at ${index + 1}`)
            logEntries(index + 1)
          }
        }).catch(error => { console.log(error) })
      }
    }).catch(error => { console.log(error) })
  }).catch(error => { console.log(error) })
}

function initializeStat (formData, index) {
  const text = entries.value.content[index][1]
  const options = entries.value.content[index][0]
  console.log('Posting a Stat Creation event paragraph.')
  axios.post('api/v1/create-eventparagraph/', formData).then(response => {
    console.log(`Posted Stat Creation Reference Paragraph at Index: ${index + 0.65}.`)
    const referenceParagraph = response.data.id
    axios.get('api/v1/create-player/', { params: { chapter: chapter.value, name: options.player, paragraph: referenceParagraph } }).then(response => {
      const relevantPlayer = response.data
      console.log('Creating new Stat: ', options.name)
      const newStatFormData = {
        player: relevantPlayer.id,
        name: options.name,
        referenceParagraph: referenceParagraph,
        base: options.base,
        increased: options.increased,
        trained: options.trained,
        bar: options.bar
      }
      axios.post('api/v1/create-stat/', newStatFormData).then(response => {
        const newStat = response.data
        console.log('Created new stat: ', newStat.name)
        if (text !== '') {
          const additionalParagraphFormData = {
            chapter: chapter.value,
            text: text,
            textorder: index + 0.0
          }
          console.log('Posting additional text paragraph.')
          axios.post('api/v1/create-paragraph/', additionalParagraphFormData).then(response => {
            console.log(`Posted additional paragraph ${response.data} at index: ${index + 0.0}. Now posting at ${index + 1}`)
            logEntries(index + 1)
          }).catch(error => { console.log(error) })
        } else {
          console.log(`Now posting at ${index + 1}`)
          logEntries(index + 1)
        }
      }).catch(error => { console.log(error) })
    }).catch(error => { console.log(error) })
  }).catch(error => { console.log(error) })
}

function initializeSkill (formData, index) {
  const text = entries.value.content[index][1]
  const options = entries.value.content[index][0]
  console.log('Posting a Skill Creation event paragraph.')
  axios.post('api/v1/create-eventparagraph/', formData).then(response => {
    console.log(`Posted Skill Creation Reference Paragraph at Index: ${index + 0.66}.`)
    const referenceParagraph = response.data.id
    axios.get('api/v1/create-player/', { params: { chapter: chapter.value, name: options.player, paragraph: referenceParagraph } }).then(response => {
      const relevantPlayer = response.data
      console.log('Retrieving latest stat instance.')
      axios.get('api/v1/create-stat/', { params: { route: 'statByName', statName: options.modifier, playerName: options.player, chapter: chapter.value, paragraph: referenceParagraph } }).then(response => {
        const relevantStat = response.data
        console.log('Creating new Skill: ', options.name)
        const newSkillFormData = {
          player: relevantPlayer.id,
          modifier: relevantStat.id,
          name: options.name,
          referenceParagraph: referenceParagraph,
          level: options.level,
          exp: options.exp,
          description: options.description,
          typ: options.typ,
          ap: options.ap
        }
        axios.post('api/v1/create-skill/', newSkillFormData).then(response => {
          const newSkill = response.data
          console.log('Created new skill: ', newSkill.name)
          if (text !== '') {
            const additionalParagraphFormData = {
              chapter: chapter.value,
              text: text,
              textorder: index + 0.0
            }
            console.log('Posting additional text paragraph.')
            axios.post('api/v1/create-paragraph/', additionalParagraphFormData).then(response => {
              console.log(`Posted additional paragraph ${response.data} at index: ${index + 0.0}. Now posting at ${index + 1}`)
              logEntries(index + 1)
            }).catch(error => { console.log(error) })
          } else {
            console.log(`Now posting at ${index + 1}`)
            logEntries(index + 1)
          }
        }).catch(error => { console.log(error) })
      }).catch(error => { console.log(error) })
    }).catch(error => { console.log(error) })
  }).catch(error => { console.log(error) })
}

function initializeQuest (formData, index) {
  const text = entries.value.content[index][1]
  const options = entries.value.content[index][0]
  console.log('Posting a Quest Creation event paragraph.')
  axios.post('api/v1/create-eventparagraph/', formData).then(response => {
    console.log(`Posted Quest Creation Reference Paragraph at Index: ${index + 0.61}.`)
    const referenceParagraph = response.data.id
    axios.get('api/v1/create-player/', { params: { chapter: chapter.value, name: options.player, paragraph: referenceParagraph } }).then(response => {
      const relevantPlayer = response.data
      console.log('Creating new Quest: ', options.name)
      const newQuestFormData = {
        player: relevantPlayer.id,
        name: options.name,
        referenceParagraph: referenceParagraph,
        statusOfQuest: 'Unlocked',
        description: options.description,
        optional_description: options.optional_description,
        tier: options.tier,
        difficulty: options.difficulty,
        reward_title: options.reward_title,
        reward: options.reward,
        optional_reward: options.optional_reward,
        exp_received: 0.00
      }
      axios.post('api/v1/create-quest/', newQuestFormData).then(response => {
        const newQuest = response.data
        console.log('Created new Quest: ', newQuest.name)
        if (text !== '') {
          const additionalParagraphFormData = {
            chapter: chapter.value,
            text: text,
            textorder: index + 0.0
          }
          console.log('Posting additional text paragraph.')
          axios.post('api/v1/create-paragraph/', additionalParagraphFormData).then(response => {
            console.log(`Posted additional paragraph ${response.data} at index: ${index + 0.0}. Now posting at ${index + 1}`)
            logEntries(index + 1)
          }).catch(error => { console.log(error) })
        } else {
          console.log(`Now posting at ${index + 1}`)
          logEntries(index + 1)
        }
      }).catch(error => { console.log(error) })
    }).catch(error => { console.log(error) })
  }).catch(error => { console.log(error) })
}

function initializeRelationship (formData, index) {
  const text = entries.value.content[index][1]
  const options = entries.value.content[index][0]
  console.log('Posting a Relationship Creation event paragraph.')
  axios.post('api/v1/create-eventparagraph/', formData).then(response => {
    console.log(`Posted Relationship Creation Reference Paragraph at Index: ${index + 0.71}.`)
    const referenceParagraph = response.data.id
    axios.get('api/v1/create-player/', { params: { chapter: chapter.value, name: options.player, paragraph: referenceParagraph } }).then(response => {
      const relevantPlayer = response.data
      axios.get('api/v1/create-character/', { params: { name: options.npc.split(' ')[0], lastname: options.npc.split(' ')[1], chapter: chapter.value, paragraph: referenceParagraph } }).then(response => {
        const relevantCharacter = response.data
        console.log(`Creating new Relationship of: ${options.player} with ${options.npc}`)
        const newRelationshipFormData = {
          player: relevantPlayer.id,
          npc: relevantCharacter.id,
          referenceParagraph: referenceParagraph,
          description: options.description,
          score: options.score
        }
        axios.post('api/v1/create-relationship/', newRelationshipFormData).then(response => {
          const newRelationship = response.data
          console.log(`Created new ${newRelationship} of: ${options.player} with ${options.npc}`)
          if (text !== '') {
            const additionalParagraphFormData = {
              chapter: chapter.value,
              text: text,
              textorder: index + 0.0
            }
            console.log('Posting additional text paragraph.')
            axios.post('api/v1/create-paragraph/', additionalParagraphFormData).then(response => {
              console.log(`Posted additional paragraph ${response.data} at index: ${index + 0.0}. Now posting at ${index + 1}`)
              logEntries(index + 1)
            }).catch(error => { console.log(error) })
          } else {
            console.log(`Now posting at ${index + 1}`)
            logEntries(index + 1)
          }
        }).catch(error => { console.log(error) })
      }).catch(error => { console.log(error) })
    }).catch(error => { console.log(error) })
  }).catch(error => { console.log(error) })
}

function initializeItem (formData, index) {
  const text = entries.value.content[index][1]
  const options = entries.value.content[index][0]
  console.log('Posting a Item Creation event paragraph.')
  axios.post('api/v1/create-eventparagraph/', formData).then(response => {
    console.log(`Posted Item Creation Reference Paragraph at Index: ${index + 0.61}.`)
    const referenceParagraph = response.data.id
    console.log('Retrieving relevant Character...')
    const name = options.belongsTo.split(' ')
    console.log('Name is: ', name)
    axios.get('api/v1/create-character/', { params: { name: options.belongsTo.split(' ')[0], lastname: options.belongsTo.split(' ')[1], chapter: chapter.value, paragraph: referenceParagraph } }).then(response => {
      const referenceCharacter = response.data[0]
      console.log('Relevant character is: ', referenceCharacter)
      console.log('Creating new Item: ', options.name)
      const isEquipped = options.isEquipped == 'True' ? true : false
      const inInventory = !isEquipped
      const newItemFormData = {
        name: options.name,
        chapter: chapter.value,
        referenceParagraph: referenceParagraph,
        typ: options.typ,
        slot: options.slot,
        quantity: parseInt(options.quantity),
        creator: options.creator,
        rarity: options.rarity,
        appearance: options.appearance,
        details: options.details,
        attributes: options.attributes,
        charge: parseInt(options.charge),
        durability: parseInt(options.durability),
        belongsTo: referenceCharacter.id,
        isEquipped: isEquipped,
        inInventory: inInventory,
        sellValue: parseInt(options.sellValue)
      }
      axios.post('api/v1/create-item/', newItemFormData).then(response => {
        const newItem = response.data
        console.log('Created new Item: ', newItem.name)
        if (text !== '') {
          const additionalParagraphFormData = {
            chapter: chapter.value,
            text: text,
            textorder: index + 0.0
          }
          console.log('Posting additional text paragraph.')
          axios.post('api/v1/create-paragraph/', additionalParagraphFormData).then(response => {
            console.log(`Posted additional paragraph ${response.data} at index: ${index + 0.0}. Now posting at ${index + 1}`)
            logEntries(index + 1)
          }).catch(error => { console.log(error) })
        } else {
          console.log(`Now posting at ${index + 1}`)
          logEntries(index + 1)
        }
      }).catch(error => { console.log(error) })
    }).catch(error => { console.log(error) })
  }).catch(error => { console.log(error) })
}

// // initializeInventory
// function initializeInventory (formData, index) {
//   const text = entries.value.content[index][1]
//   const options = entries.value.content[index][0]
//   console.log('Posting a Inventory Creation event paragraph.')
//   axios.post('api/v1/create-eventparagraph/', formData).then(response => {
//     console.log(`Posted Inventory Creation Reference Paragraph at Index: ${index + 0.63}.`)
//     const referenceParagraph = response.data.id
//     console.log(options)
//     axios.get('api/v1/create-player/', { params: { chapter: chapter.value, name: options.player, paragraph: referenceParagraph } }).then(response => {
//       const relevantPlayer = response.data
//       console.log('Creating new Inventory for: ', options.player)
//       const newInventoryFormData = {
//         player: relevantPlayer.id,
//         referenceParagraph: referenceParagraph,
//         referenceToLastRelevantEvent: 0,
//         description: options.description,
//         slots: options.slots
//       }
//       axios.post('api/v1/create-inventory/', newInventoryFormData).then(response => {
//         const newInventory = response.data
//         console.log('Created new Inventory: ', newInventory)
//         if (text !== '') {
//           const additionalParagraphFormData = {
//             chapter: chapter.value,
//             text: text,
//             textorder: index + 0.0
//           }
//           console.log('Posting additional text paragraph.')
//           axios.post('api/v1/create-paragraph/', additionalParagraphFormData).then(response => {
//             console.log(`Posted additional paragraph ${response.data} at index: ${index + 0.0}. Now posting at ${index + 1}`)
//             logEntries(index + 1)
//           }).catch(error => { console.log(error) })
//         } else {
//           console.log(`Now posting at ${index + 1}`)
//           logEntries(index + 1)
//         }
//       }).catch(error => { console.log(error) })
//     }).catch(error => { console.log(error) })
//   }).catch(error => { console.log(error) })
// }

// // initializeSlot
// function initializeSlot (formData, index) {
//   const text = entries.value.content[index][1]
//   const options = entries.value.content[index][0]
//   console.log('Posting a Slot Creation event paragraph.')
//   axios.post('api/v1/create-eventparagraph/', formData).then(response => {
//     console.log(`Posted Slot Creation Reference Paragraph at Index: ${index + 0.635}.`)
//     const referenceParagraph = response.data.id
//     console.log('Retrieving inventory of player ', options.player)
//     axios.get('api/v1/create-inventory/', { params: { chapter: chapter.value, player: options.player, paragraph: referenceParagraph } }).then(response => {
//       const relevantInventory = response.data
//       console.log(relevantInventory)
//       console.log('Retrieving item instance of: ', options.item)
//       axios.get('api/v1/create-item', { params: { chapter: chapter.value, itemName: options.item, paragraph: referenceParagraph } }).then(response => {
//         const relevantItem = response.data
//         console.log(relevantItem)
//         console.log('Creating new Slot in inventory with ', relevantItem.name)
//         const newSlotFormData = {
//           inventory: relevantInventory.id,
//           referenceParagraph: referenceParagraph,
//           referenceToLastRelevantEvent: 0,
//           item: relevantItem.id
//         }
//         axios.post('api/v1/create-slot/', newSlotFormData).then(response => {
//           console.log('Posted new slot: ', response.data)
//           if (text !== '') {
//             const additionalParagraphFormData = {
//               chapter: chapter.value,
//               text: text,
//               textorder: index + 0.0
//             }
//             console.log('Posting additional text paragraph.')
//             axios.post('api/v1/create-paragraph/', additionalParagraphFormData).then(response => {
//               console.log(`Posted additional paragraph ${response.data} at index: ${index + 0.0}. Now posting at ${index + 1}`)
//               logEntries(index + 1)
//             }).catch(error => { console.log(error) })
//           } else {
//             console.log(`Now posting at ${index + 1}`)
//             logEntries(index + 1)
//           }
//         }).catch(error => { console.log(error) })
//       })
//     }).catch(error => { console.log(error) })
//   }).catch(error => { console.log(error) })
// }

// // initializeEquipment
// function initializeEquipment (formData, index) {
//   const text = entries.value.content[index][1]
//   const options = entries.value.content[index][0]
//   console.log('Posting a Equipment Creation event paragraph.')
//   axios.post('api/v1/create-eventparagraph/', formData).then(response => {
//     console.log(`Posted Equipment Creation Reference Paragraph at Index: ${index + 0.63}.`)
//     // Problem: die Felder sollten nicht undefined sein, sondern später belegt werden. Dafür bräuchte ich
//     // models, serializer, view, signals, etc. für alle equipment slots einzeln.
//     // BEFORE CONTINUING WITH THIS:
//     // ensure that the design of the database and character/player structure as exported from database
//     // to chapter works as intended. => create the functions to populate player sheets etc according to
//     // scroll behavior!
//     const referenceParagraph = response.data.id
//     axios.get('api/v1/create-player/', { params: { chapter: chapter.value, name: options.player, paragraph: referenceParagraph } }).then(response => {
//       const relevantPlayer = response.data
//       console.log('Creating new Equipment for: ', options.player)
//       const newInventoryFormData = {
//         player: relevantPlayer.id,
//         referenceParagraph: referenceParagraph,
//         description: options.description,
//         slots: options.slots
//       }
//       axios.post('api/v1/create-inventory/', newInventoryFormData).then(response => {
//         const newInventory = response.data
//         console.log('Created new Inventory: ', newInventory)
//         if (text !== '') {
//           const additionalParagraphFormData = {
//             chapter: chapter.value,
//             text: text,
//             textorder: index + 0.0
//           }
//           console.log('Posting additional text paragraph.')
//           axios.post('api/v1/create-paragraph/', additionalParagraphFormData).then(response => {
//             console.log(`Posted additional paragraph ${response.data} at index: ${index + 0.0}. Now posting at ${index + 1}`)
//             logEntries(index + 1)
//           }).catch(error => { console.log(error) })
//         } else {
//           console.log(`Now posting at ${index + 1}`)
//           logEntries(index + 1)
//         }
//       }).catch(error => { console.log(error) })
//     }).catch(error => { console.log(error) })
//   }).catch(error => { console.log(error) })
// }

// initializeCurrency
// initializeParagon
// initializePact
// initializeMonster???

function logout () {
  axios
    .post('api/v1/token/logout', null, {
      headers: {
        Authorization: `Token ${localStorage.getItem('token')}`
      }
    })
    .then(response => {
      console.log(response.data)
      axios.defaults.headers.common.Authorization = ''
      localStorage.removeItem('token')
      localStorage.removeItem('username')
      localStorage.removeItem('userid')
      console.log('Logged out successfully!')
    })
    .catch(error => {
      console.log(JSON.stringify(error))
    })

  accountStore.removeToken()
  router.push('/login')
}

function navigateToCurrentChapter () {
  const chapter = route.params[chapterStore.currentChapter]
  router.push(chapter ? `/chapter/${chapter}` : '/')
}

// function navigateToGraphs () {
//   router.push('/graphs/')
// }

function calcExp (msg) {
  const lvl = parseInt(msg.level)
  const power = parseInt(msg.power)
  const difficulty = parseInt(msg.difficulty)
  const tier = parseInt(msg.tier)
  const typ = msg.type
  const base = 1.00
  let reward
  if (typ === 'monster') {
    if (lvl === 0) {
      return base
    }
    switch (tier) {
      case 1:
        console.log('We are trying to post a monster kill: ', msg)
        // console.log('level: ', lvl)
        // console.log('power: ', power)
        // console.log('tier: ', tier)
        reward = base * Math.pow((power * 3) / (Math.pow(lvl, 0.5) + 10) + 6, 6) / Math.pow(lvl * 2, 2) / 900000
        return reward.toFixed(4)
      default:
        reward = 0.00
        return reward
    }
  } else if (typ === 'achievement' || typ === 'quest') {
    console.log('We are trying to post an achievement or quest: ', msg)
    // console.log('level: ', lvl)
    // console.log('difficulty: ', difficulty)
    // console.log('tier: ', tier)
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
        // console.log('Calculated exp is: ', reward)
        return reward
      case 1: // power = difficulty!
        reward = base * base / 3 * Math.pow(difficulty, 2) / Math.pow(lvl, 2) / 45 * lvl
        return reward
      default:
        reward = base * base * Math.pow(difficulty, 2) / Math.pow(lvl, 2)
        return reward
    }
  } else {
    return 0.00
  }
}

function calcProgressExp (statLevel, amountSpent, stat) {
  const total = parseInt(stat.base) + parseInt(stat.increased) + parseFloat(stat.trained)
  if (parseInt(amountSpent) >= 0) {
    return statLevel
  }
  const cost = Math.abs(parseInt(amountSpent))
  const spentPercentage = cost / total
  const base = 100
  let reward = 0
  // if (statLevel === 0) {
  //   return statLevel + 1
  // }
  reward = base * Math.pow((cost * 3) / (Math.pow(statLevel, 0.1) + 5) + 0.1, 2.1) / Math.pow((statLevel + 1) * 2, 2) / 10
  const newLevel = reward / (1 + reward) * spentPercentage + Math.log10(statLevel + 2) * spentPercentage * 1 / (1 + statLevel)
  // console.log('Level: ', statLevel)
  // console.log('Amount: ', cost)
  // console.log('Base: ', parseInt(stat.base))
  // console.log('Increased: ', parseInt(stat.increased))
  // console.log('Trained: ', parseFloat(stat.trained))
  // console.log('Total: ', total)
  // console.log('Percentage: ', spentPercentage)
  // console.log('reward: ', reward)
  // console.log('newLevel: ', newLevel)
  return statLevel + newLevel
}

function returnReward (level) {
  const points = calcStatPointsOnLevel(level)
  let paragon = ''
  if (level === 10) {
    paragon = `Paragon System Unlocked!
    +1 Paragon Point`
  } else if (level > 10) {
    paragon = '+1 Paragon Point'
  } else if (level === 1) {
    paragon = '+1 Skill Point'
  }
  const returnString = `+${points} Stat Points
  ${paragon}`
  return returnString
}

function calcStatPointsOnLevel (lvl) {
  const statpoints = Math.round(lvl + Math.pow(Math.floor(lvl / 10), Math.log(lvl * 2)))
  return statpoints
}

function capitalizeString (str) {
  const prepositions = ['to', 'of', 'from', 'in', 'on', 'at', 'by', 'with', 'for', 'over']
  const words = str.split(' ')
  const capitalizedWords = words.map((word, index) => {
    if (index === 0) {
      return word.charAt(0).toUpperCase() + word.slice(1)
    } else if (prepositions.includes(word.toLowerCase())) {
      return word.toLowerCase()
    } else {
      return word.charAt(0).toUpperCase() + word.slice(1)
    }
  })
  return capitalizedWords.join(' ')
}

function findCost (options) {
  let cost = 0
  cost = Object.hasOwn(options, 'ap') ? options.ap : cost
  cost = Object.hasOwn(options, 'mp') ? options.mp : cost
  cost = Object.hasOwn(options, 'st') ? options.st : cost
  // console.log('Cost: ', cost)
  return parseInt(cost)
}

</script>
