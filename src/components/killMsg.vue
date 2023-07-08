<template>
  <div class="text-white py-1 my-3 mx-6 text-sm text-center border-y">
    You have killed [<span class="text-red-500">{{ props.p['text'] }}</span>]! 
    Reward: <span class="text-green-400">{{ returnExp(props.p['exp']) }}</span>% Exp
  </div>
</template>

<script setup>

const props = defineProps({
  p: {
    type: Object,
    default: () => ({})
  }
})

function returnExp (exp) {
  const percentage = exp * 100
  return percentage.toFixed(2)
}

</script>
