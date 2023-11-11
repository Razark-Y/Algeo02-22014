<template>
    <!-- <div class="relative">
        <img :src="getImageURL(imgJson['imageTitle'])" alt="" class="w-40 h-40">
        <div class="absolute text-sm font-semibold text-white bottom-4 left-1/2 -translate-x-1/2">
            {{ imgJson['similarity'] }}
        </div>
    </div> -->
    <div class="w-40 h-40 bg-cover flex justify-center items-end" :style="`background-image: url(${getImageURL(imgJson['imageTitle'])});`">
        <div class="text-center text-sm font-semibold text-white w-full pb-1.5 pt-1" style="background-color: rgba(0, 0, 0, .5);" >
            {{ parseFloat(imgJson['similarity']).toFixed(2) }}
        </div>
    </div>
</template>

<script setup>
    defineProps({
        imgJson:Object
    })
    
    function getImageURL(name) {
        return new URL(`../assets/img/${name}`,import.meta.url).href
    }

</script>

<style scoped>

</style>