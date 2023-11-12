<template>
  <!-- 
NOTE!!!
Pagination masih maksa
-->
  <div class="flex flex-col justify-center items-center gap-8 mb-4 mt-5">
    <h1 class="font-bold text-3xl">Reverse Image Search</h1>
    <div class="flex gap-5">
      <div
        class="bg-slate-400 w-60 h-50 bg-contain bg-center rounded-sm shadow-xl"
        :style="`background-image: url(${imageURL});`"
        style="background-repeat: no-repeat"
      ></div>
      <div>
        <form method="POST" enctype="multipart/form-data">
          <div class="flex flex-col items-center">
            <label
              for="image"
              class="text-lg text-white font-bold bg-orange-500 px-3 py-1 rounded-md cursor-pointer hover:grayscale text-center mb-12"
              >Image Input
              <input
                type="file"
                id="image"
                name="image"
                accept="image/*"
                class="hidden"
                @change="changeListener"
              />
            </label>

            <div class="flex flex-col justify-center mb-3">
              <label for="toogleButton" class="flex flex-col gap-1 items-center cursor-pointer">
                <div v-if="!tipeInput" class="px-2 font-thin">Color</div>
                <div v-else class="px-2 font-thin">Texture</div>
                <!-- toggle -->
                <div class="relative">
                  <input
                    @click="changeUrl"
                    id="toogleButton"
                    type="checkbox"
                    class="hidden"
                    v-model="tipeInput"
                  />
                  <!-- path -->
                  <div class="toggle-path bg-yellow-400 w-9 h-5 rounded-full shadow-inner"></div>
                  <!-- crcle -->
                  <div
                    class="toggle-circle absolute w-3.5 h-3.5 bg-white rounded-full shadow inset-y-0 left-0"
                  ></div>
                </div>
              </label>
            </div>

            <button
              v-bind:disabled="!isButtonClickable || isUploading"
              type="submit"
              :class="{ disabled: !isButtonClickable || isUploading }"
              class="group relative h-12 w-48 overflow-hidden rounded-2xl bg-green-500 text-lg text-white font-bold text-whiteg-orange-300 px-3 py-1"
              @click.prevent="uploadFile"
            >
              Search
              <div
                class="absolute inset-0 h-full w-full scale-0 rounded-2xl transition-all duration-300 group-hover:scale-100 group-hover:bg-white/30"
              ></div>
            </button>
          </div>
        </form>
      </div>
    </div>

    <div id="addDatabase">
      <form method="POST" enctype="multipart/form-data">
        <div class="flex flex-row gap-4 items-center h-fit">
          <button
            @click.prevent="uploadDB"
            v-bind:disabled="!isButtonClickable || isUploading"
            :class="{ disabled: !isButtonClickable || isUploading }"
            class="px-4 py-2 bg-green-700 text-md text-white font-bold rounded-md hover:grayscale"
          >
            Upload Database
          </button>
          <div
            v-if="!isHidden"
            id="statusLight"
            class="w-4 h-4 rounded-full "
            :class="{ 'bg-green-400 animate-bounce': isUploaded, 'bg-yellow-400 animate-ping': !isUploaded }"
          ></div>
        </div>
      </form>
    </div>

    <div class="flex flex-row flex-wrap justify-center gap-8 mx-40 max-w-2xl">
      <Gambar
        v-for="(value, key) in pagedImageData[currentPage]"
        :key="key"
        :img-json="value"
      ></Gambar>
    </div>

    <div id="paginationbar" class="flex flex-row flex-wrap gap-10">
      <div
        v-for="value in pagedImageData.length"
        :key="value"
        class="hover:cursor-pointer hover:scale-125"
        @click="changePage(value - 1)"
      >
        {{ value }}
      </div>
    </div>
  </div>
</template>

<script setup>
import Gambar from './components/gambar-viewer.vue'
import axios from 'axios'
import { ref, computed } from 'vue'
const isUploading = ref(false);
const isButtonClickable = ref(false)
const isHidden = ref(true)
const isUploaded = ref(false)
const currentPage = ref(0)
const tipeInput = ref(false)
const imageInput = ref([])
const imageData = ref([])
const imageURL = ref()
const urlToSend = ref('http://127.0.0.1:5000/uploadColor')

function changeUrl() {
  if (tipeInput.value === true) {
    urlToSend.value = 'http://127.0.0.1:5000/uploadColor'
  } else {
    urlToSend.value = 'http://127.0.0.1:5000/uploadTexture'
  }
}

function changePage(value) {
  currentPage.value = value
}

const sortedImageData = computed(() => {
  // eslint-disable-next-line vue/no-side-effects-in-computed-properties
  return imageData.value
    .filter((obj) => obj['similarity'] > 60)
    .sort((a, b) => parseInt(b['similarity']) - parseInt(a['similarity']))
})

// const sortedImageData = computed(() =>{
//   // eslint-disable-next-line vue/no-side-effects-in-computed-properties
//   return imageData.value.sort((a,b) => parseInt(b['similarity']) - parseInt(a['similarity']))
// })

const pagedImageData = computed(() => {
  let data = []
  let subData = []
  let inLoop = false
  for (let i = 0; i < sortedImageData.value.length; i++) {
    inLoop = true
    subData.push(sortedImageData.value[i])
    if ((i + 1) % 9 == 0) {
      data.push(subData)
      subData = []
    }
  }
  if (subData != [] && inLoop) {
    data.push(subData)
  }
  return data
})

function changeListener(e) {
  isButtonClickable.value = true
  isHidden.value = true
  imageInput.value = e.target.files[0]
  imageURL.value = URL.createObjectURL(e.target.files[0])
}

const uploadFile = async () => {
  isUploading.value = true;
  isHidden.value = false
  isUploaded.value = false
  const formData = new FormData()
  formData.append('image', imageInput.value)
  try {
    const response = await axios.post(urlToSend.value, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    console.log(response.data)
    imageData.value = response.data
    isUploaded.value = true
  } catch (error) {
    console.error(error)
  }
  isUploading.value = false;
}

const uploadDB = async () => {
  isUploading.value = true;
  isHidden.value = false
  isUploaded.value = false
  const formData = new FormData()
  formData.append('imageDB', imageInput.value)
  try {
    const response = await axios.post('http://127.0.0.1:5000/uploadDB', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    console.log(response.data)
    imageData.value = response.data
    isUploaded.value = true
  } catch (error) {
    console.error(error)
  }
  isUploading.value = false;
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

<style scope>
.disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.toggle-path {
  transition: background 0.3s ease-in-out;
}
.toggle-circle {
  top: 0.2rem;
  left: 0.25rem;
  transition: all 0.3s ease-in-out;
}
input:checked ~ .toggle-circle {
  transform: translateX(100%);
}
input:checked ~ .toggle-path {
  background-color: #81e6d9;
}
</style>
