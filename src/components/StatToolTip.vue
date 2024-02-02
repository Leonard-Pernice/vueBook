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
    <div 
      ref="floatingRef"
      :class="['absolute top-0 left-0 z-50 bg-gradient-radial from-gr-inner-blue to-gr-outer-blue text-sm text-white px-3 py-1.5 rounded-md cursor-default border-2 border-blue-400', isHidden && 'hidden']">
      Name: {{ props.stat.name }}
      <div name="STAT TOTAL" class="flex justify-center">
        <div class="grid grid-cols-2 border border-white w-auto">
          <div class="px-1 py-1 text-xs border-b border-white">Total:</div>
          <div class="px-1 py-1 text-xs border-b border-white flex justify-center">{{ getTotal(props.stat) }}</div>
          <div class="px-1 py-1 text-xs border-b border-white">Base value at creation: :</div>
          <div class="px-1 py-1 text-xs border-b border-white flex justify-center">{{ props.stat.base }}</div>
          <div class="px-1 py-1 text-xs border-b border-white">Increased via Statpoints:</div>
          <div class="px-1 py-1 text-xs border-b border-white flex justify-center">{{ props.stat.increased }}</div>
          <div class="px-1 py-1 text-xs">Manually trained:</div>
          <div class="px-1 py-1 text-xs flex justify-center">{{ props.stat.trained }}</div>
        </div>
      </div>
      <div ref="arrowRef" class="absolute bg-gr-inner-blue h-2 w-2 rotate-45 border-2 border-blue-400"></div>
    </div>
  </div>
  </template>

<script setup>
import { arrow, computePosition, flip, offset, shift } from '@floating-ui/dom'
import { ref } from 'vue'
import { calcAccumulatedStatPoints, statAbreviations } from '@/help/extraFunctions.js'

const props = defineProps({
  stat: {
    type: Object,
    default: {}
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

function getTotal (stat) {
  return stat.base + stat.increased + Math.floor(stat.trained)
}

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

function hide () {
  isHidden.value = true
}

function show () {
  isHidden.value = false
  calculatePosition()
}

</script>
