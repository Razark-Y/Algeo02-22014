<template>
  <div class="flex flex-col justify-center items-center">
    <h1 class="font-bold">Reverse Image Search</h1>
    <div class="flex gap-5">
      <img src="" alt="uploadedimage">
      <div >
        <form action="http://127.0.0.1:5000/upload" method="POST" enctype="multipart/form-data">
          <div class="flex flex-col">
            <label for="image" class="bg-orange-500 px-3 py-1 rounded-md cursor-pointer">Image Input
              <input type="file" id="image" name="image" accept="image/*">
            </label>
            <label for="tipeCBIR">Color / Texture</label>
            <input type="checkbox" name="tipeCBIR" id="">
            <button type="submit" class="bg-orange-300 px-3 py-1">Search</button>
          </div>
        </form>
      </div>
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