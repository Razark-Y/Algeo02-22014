<template>
  <div
    class="w-40 h-40 bg-cover flex justify-center items-end rounded-lg overflow-clip shadow-lg"
    :style="`background-image: url(${imageData});`"
  >
    <div
      class="text-center text-sm font-semibold text-white w-full pb-1.5 pt-1"
      style="background-color: rgba(0, 0, 0, 0.5)"
    >
      {{ parseFloat(imgJson['similarity']).toFixed(2) }}
    </div>
  </div>
</template>

<script setup>
import {ref,onMounted,toRefs} from 'vue'
const props = defineProps({
  imgJson: Object
})

const {imgJson} = toRefs(props)

const imageData = ref()
onMounted(()=>{
  imageData.value = `data:image/jpeg;base64,${imgJson.value['imageTitle']}`
})
</script>

<style scoped></style>
