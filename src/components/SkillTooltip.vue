<template>
    <div class="">
      <div
          @mouseenter="show"
          @mouseleave="hide"
          @focus="show"
          @blur="hide"
          ref="referenceRef"
          class="">
          <slot/>
      </div>
      <div ref="floatingRef" :class="['absolute top-0 left-0 z-50 bg-gradient-radial from-gr-inner-blue to-gr-outer-blue text-sm text-white px-3 py-1.5 rounded-md cursor-default border-2 border-cyan-500', isHidden && 'hidden']">
        <div class="border-b grid grid-cols-3 h-10 p-4 text-2xl">
            <div class="border-white">
                <GlowText :content="props.skill.name"></GlowText>
            </div>
            <div class="border-white">
                <GlowText :content="props.skill.typ"></GlowText>
            </div>
            <div class="border-white">
                <GlowText :content="'Level: ' + props.skill.level"></GlowText>
            </div>
            <div class="border-white">{{ findCost(props.skill) }}</div>
            <div class="border-white">EXP: </div>
            <div name="EXP BAR" class="flex grow h-full bg-gray-200">
              <div class="h-inherit bg-blue-600 text-xs font-medium text-blue-100 text-center p-0.5 leading-none" :style="{ width: (props.skill.exp)+'%' }"></div>
            </div>
            <div class="col-span-3">{{ props.skill.description }}</div>
        </div>
        <div ref="arrowRef" class="absolute bg-gr-inner-blue h-2 w-2 rotate-45 border-2 border-cyan-500"></div>
      </div>
    </div>
</template>
  
  <script setup>
  import { arrow, computePosition, flip, offset, shift } from '@floating-ui/dom'
  import { ref } from 'vue'
  import GlowText from './GlowText.vue'
  
  const props = defineProps({
    skill: {
      type: Object
    },
    placement: {
      type: String,
      default: 'right'
    }
  })
  
  const referenceRef = ref()
  const floatingRef = ref()
  const arrowRef = ref()
  const isHidden = ref(true)
  
  async function calculatePosition () {
    const { x, y, middlewareData, placement } = await computePosition(referenceRef.value, floatingRef.value, {
      placement: props.placement,
      middleware: [
        offset(8),
        flip(),
        shift({ padding: 5 }),
        arrow({ element: arrowRef.value })
      ]
    })
  
    Object.assign(floatingRef.value.style, {
      left: `${x}px`,
      top: `${y}px`
    })
  
    const { x: arrowX, y: arrowY } = middlewareData.arrow
  
    const opposedSide = {
      left: 'right',
      right: 'left',
      bottom: 'top',
      top: 'bottom'
    }[placement.split('-')[0]]
  
    Object.assign(arrowRef.value.style, {
      left: arrowX ? `${arrowX}px` : '',
      top: arrowY ? `${arrowY}px` : '',
      bottom: '',
      right: '',
      [opposedSide]: '-5px'
    })
  }
  
  function findCost (skill) {
    const costs = ['ap', 'mp', 'st']
    for (const cost of costs) {
        if (skill[cost] != 0) {
            return 'Cost: ' + skill[cost] + ' ' + cost
        }
    }
    return 'Cost: None'
  }

  function hide () {
    isHidden.value = true
  }
  
  function show () {
    isHidden.value = false
    calculatePosition()
  }
  
  </script>
  