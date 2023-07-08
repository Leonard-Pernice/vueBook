<template>
  <div class="relative flex items-center justify-center w-full h-full text-center">
    <div class="absolute block text-blue-400 blur">{{ props.content }}</div>
    <div class="absolute block text-blue-300">{{ props.content }}</div>
    <div class="absolute block mix-blend-overlay">{{ props.content }}</div>
  </div>
</template>

<script setup>

const props = defineProps({
  content: {
    type: String,
    default: ''
  }
})
</script>
