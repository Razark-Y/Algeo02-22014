<template>
  <div class="flex flex-col justify-center items-center gap-8">
    <h1 class="font-bold text-3xl">Reverse Image Search</h1>    
    <div class="flex gap-5">
      <div  class="bg-slate-500 w-60 h-40 bg-contain bg-center" :style="`background-image: url(${imageURL});`" style="background-repeat: no-repeat;">
      </div>
      <div >
        <form method="POST" enctype="multipart/form-data">
          <div class="flex flex-col items-center">
            <label for="image" class="text-lg text-white font-bold bg-orange-500 px-3 py-1 rounded-md cursor-pointer hover:grayscale text-center mb-12">Image Input
              <input type="file" id="image" name="image" accept="image/*" class="hidden" @change="changeListener">
            </label>

            <div id="chooseCBIR" class="flex gap-4 justify-center align-middle mb-3">
              <div class="flex gap-2 hover:cursor-pointer">
                <input @click="changeUrl" type="radio" id="color" name="tipeCBIR" value="Color" v-model="tipeInput">
                <label for="color">Color</label>
              </div>
              <div class="flex gap-2">
                <input @click="changeUrl" type="radio" id="texture" name="tipeCBIR" value="Texture" v-model="tipeInput">
                <label for="texture">Texture</label>
              </div>
            </div>
            <button type="submit" class="group relative h-12 w-48 overflow-hidden rounded-2xl bg-green-500 text-lg text-white font-bold text-whiteg-orange-300 px-3 py-1" @click.prevent="uploadFile">
              Search
              <div class="absolute inset-0 h-full w-full scale-0 rounded-2xl transition-all duration-300 group-hover:scale-100 group-hover:bg-white/30"></div>
            </button>
          </div>
        </form>
      </div>
    </div>

    <div class="flex flex-row flex-wrap justify-center gap-8 mt-8">
      <Gambar v-for="(value,key) in pagedImageData[currentPage]" :key="key" :img-json="value"></Gambar>
    </div>

    <div id="paginationbar" class="flex flex-row gap-10">
      <div v-for="(value) in pagedImageData.length" key="value" class="hover:cursor-pointer" @click="changePage(value-1)">
        {{ value }}
      </div>
    </div>

  </div>

</template>

<script setup>
import Gambar from "./components/gambar-viewer.vue"
import axios from 'axios'
import { ref,computed } from 'vue';
const currentPage = ref(1);
const tipeInput = ref('Color');
const imageInput = ref([]);
const imageData = ref([]);
const imageURL = ref();
const urlToSend = ref("http://127.0.0.1:5000/uploadColor")

function changeUrl() {
  if (tipeInput.value === "Texture") {
    urlToSend.value = "http://127.0.0.1:5000/uploadColor"
  } else if (tipeInput.value === "Color"){
    urlToSend.value = "http://127.0.0.1:5000/uploadTexture"
  }
}

function changePage(value) {
  currentPage.value = value
}

// const sortedImageData = computed(() =>{
//   // eslint-disable-next-line vue/no-side-effects-in-computed-properties
//   return imageData.value.filter(obj => obj['similarity'] > 60).sort((a,b) => parseInt(b['similarity']) - parseInt(a['similarity']))
// })

const sortedImageData = computed(() =>{
  // eslint-disable-next-line vue/no-side-effects-in-computed-properties
  return imageData.value.sort((a,b) => parseInt(b['similarity']) - parseInt(a['similarity']))
})

const pagedImageData = computed(() => {
  let data = [];
  let subData = [];
  for(let i = 0; i < sortedImageData.value.length; i++) {
    subData.push(sortedImageData.value[i]);
    if((i+1) % 3 == 0) {
      data.push(subData);
      subData = [];
    }
  }
  return data
})

function changeListener(e) {
  imageInput.value = e.target.files[0];
  imageURL.value = URL.createObjectURL(e.target.files[0]);
}

const uploadFile = async () => {
  const formData = new FormData();
  formData.append('image',imageInput.value);
  try{
    const response = await axios.post(urlToSend.value,formData,{
      headers: {
        'Content-Type' : 'multipart/form-data'
      }
    });
    console.log(response.data);
    imageData.value = response.data
  } catch (error) {
    console.error(error);
  }
  // getImages();
}


// function getImages() {
//   fetch("http://127.0.0.1:5000/upload")
//   .then(response => response.json())
//   .then((data) => {
//     imageData.value = data;
//     console.log(data)
//     // console.log("Image:")
//     // console.log(imageData.value)
//   })
// }

// watch(imageData,(newValue) =>{
//   imageData.value = newValue;
// });

// function getImageURL(name) {
//   return new URL(`./assets/img/${name["imageTitle"]}`,import.meta.url).href
// }

// onMounted(() =>{
//   getImages()
// })


</script>