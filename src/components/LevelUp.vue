<template>
  <div class="flex items-center justify-center my-8">
    <div class="w-96 bg-gradient-radial from-gr-inner-blue to-gr-outer-blue text-white text-center">
      <div class="border-8 border-solid border-image-source border-image-slice m-2">
        <div class="text-xl border-b border-white mx-4">
          You have reached <span class="text-green-400">Level {{ Math.floor(props.p.exp) }}</span>!
        </div>
        <div class="my-2">You gain:
          <div class="py-2" v-for="(points, i) in props.p.text.match(/\+\d+ (Stat|Skill|Paragon) Point(s)?/g)" :key="i">
            <div class="py-1">
              <GlowText :content="points"></GlowText>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import GlowText from '@/components/GlowText.vue'

const props = defineProps({
  p: {
    type: Object
  }
})

</script>
