<template>
  <h1>Reverse Image Search</h1>
  <div>
    <img src="" alt="uploadedimage">
    <div>
      <!-- <form action="">
        <input type="file" name="image" accept="image/*">
      </form> -->

    </div>
  </div>

</template>

<script setup>
import { ref,onMounted } from 'vue';
const imageData = ref([]);

function getImages() {
  fetch("http://127.0.0.1:5000/")
  .then(response => response.json())
  .then((data) => {
    imageData.value = data;
    console.log(data)
  })
}

// function getImageURL(name) {
//   return new URL(`./assets/img/${name["imageTitle"]}`,import.meta.url).href
// }

onMounted(() =>{
  getImages()
})


</script>