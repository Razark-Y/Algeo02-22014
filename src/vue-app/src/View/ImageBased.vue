<template>
  <div class="flex flex-col justify-center items-center gap-8 mb-4 pt-24">
    <div class="flex gap-5">
      <label
        class="bg-pink-400 w-[25em] h-[18em] bg-cover bg-center rounded-sm shadow-xl flex justify-center items-center hover:cursor-pointer hover:scale-105"
        :style="`background-image: url(${imageURL});`"
        style="background-repeat: no-repeat"
        for="image"
      >
        <input
          type="file"
          id="image"
          name="image"
          accept="image/*"
          class="hidden"
          @change="changeListenerAnImage"
        />
        <div v-if="!imageURL" class="font-semibold text-white">Click Me!</div>
      </label>
      <div>
        <form method="POST" enctype="multipart/form-data">
          <div class="flex flex-col items-center">
            <div class="flex flex-col justify-end mb-3">
              <label for="toogleButton" class="flex flex-col gap-1 items-center cursor-pointer">
                <div v-if="!tipeInput" class="px-2 font-medium text-lg text-white">Color</div>
                <div v-else class="px-2 font-medium text-lg text-white">Texture</div>
                <div class="relative">
                  <input
                    @click="changeUrl"
                    id="toogleButton"
                    type="checkbox"
                    class="hidden"
                    v-model="tipeInput"
                  />
                  <div class="toggle-path bg-yellow-400 w-9 h-5 rounded-full shadow-inner"></div>
                  <div
                    class="toggle-circle absolute w-3.5 h-3.5 bg-white rounded-full shadow inset-y-0 left-0"
                  ></div>
                </div>
              </label>
            </div>

            <button
              v-bind:disabled="isUploading || !isButtonClickable || isUploading || isDB"
              type="submit"
              :class="{ disabled: isUploading || !isButtonClickable || isUploading || isDB }"
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
      <form method="POST" enctype="multipart/form-data" :on-submit="tes">
        <div class="flex flex-row gap-4 items-center h-fit">
          <label
            for="folder"
            class="text-lg text-white font-bold bg-orange-500 px-4 py-2 rounded-md cursor-pointer hover:grayscale text-center"
            >Database Input
            <input
              ref="folder"
              type="file"
              id="folder"
              name="file[]"
              class="hidden"
              @change="changeListenerFolder"
              webkitdirectory
              mozdirectory
            />
          </label>
          <button
            type="submit"
            @click.prevent="uploadDB"
            v-bind:disabled="!isButtonClickable || isUploading || isINPT"
            :class="{ disabled: !isButtonClickable || isUploading || isINPT }"
            class="px-4 py-2.5 bg-green-700 text-md text-white font-bold rounded-md hover:grayscale"
          >
            Upload Database
          </button>
          <div class="text-white">
            {{ formattedElapsedTime }}
          </div>
          <div class="text-white" v-if="!isHidden ">
            {{ sortedImageData.length }} gambar
          </div>
          <div
            v-if="!isHidden"
            id="statusLight"
            class="w-4 h-4 rounded-full"
            :class="{
              'bg-green-400': isUploaded,
              'bg-yellow-400 animate-ping': !isUploaded,
              'bg-red-600 animate-none': isError
            }"
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

    <Paginate
      v-if="pagedImageData.length != 0"
      :page-count="pagedImageData.length"
      :active-class="`text-yellow-600 scale-105 border-[#ffddd2]`"
      :page-link-class="`px-3 py-6 text-white font-semibold`"
      :prev-link-class="`px-3 py-6 text-white font-semibold`"
      :next-link-class="`px-3 py-6 text-white font-semibold`"
      :click-handler="changePage"
      :prev-text="'Prev'"
      :next-text="'Next'"
      :container-class="`flex flex-row gap-10`"
      :page-class="`border-[3px] border-[#ef6e4e] rounded-md hover:cursor-pointer hover:scale-105 transition py-2 px-2`"
      :next-class="`border-[3px] border-[#ef6e4e] rounded-md hover:cursor-pointer hover:scale-105 transition py-2 px-2`"
      :prev-class="`border-[3px] border-[#ef6e4e] rounded-md hover:cursor-pointer hover:scale-105 transition py-2 px-2`"
    >
    </Paginate>
  </div>
</template>

<script setup>
import Paginate from 'vuejs-paginate-next'
import Gambar from '../components/gambar-viewer.vue'
import axios from 'axios'
import { ref, computed } from 'vue'

// STATE
const isError = ref(false)
const isUploading = ref(false)
const isButtonClickable = ref(true)
const isHidden = ref(true)
const isUploaded = ref(false)
const currentPage = ref(0)
const tipeInput = ref(false)
const elapsedTime = ref(0)
const timer = ref(undefined)
const urlToSend = ref('http://127.0.0.1:5000/uploadColor')
const isDB = ref(false)
const isINPT = ref(false)

// DATA
const imageInput = ref([])
const folderInput = ref([])
const imageData = ref([])
const imageURL = ref()

function changeUrl() {
  if (tipeInput.value === true) {
    urlToSend.value = 'http://127.0.0.1:5000/uploadColor'
  } else {
    urlToSend.value = 'http://127.0.0.1:5000/uploadTexture'
  }
}

function changePage(value) {
  console.log(value)
  currentPage.value = parseInt(value) - 1
}

const sortedImageData = computed(() => {
  // eslint-disable-next-line vue/no-side-effects-in-computed-properties
  return imageData.value
    .filter((obj) => obj['similarity'] > 60)
    .sort((a, b) => parseFloat(b['similarity']) - parseFloat(a['similarity']))
})

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
  if (subData.length != 0 && inLoop) {
    data.push(subData)
  }
  return data
})

function changeListenerAnImage(e) {
  isError.value = false
  isINPT.value = true
  isDB.value = false
  isButtonClickable.value = true
  isHidden.value = true
  imageInput.value = e.target.files[0]
  imageURL.value = URL.createObjectURL(e.target.files[0])
  console.log(e.target.files[0])
}

function tes(e) {
  console.log(e)
}

function changeListenerFolder(e) {
  isError.value = false
  isINPT.value = false
  isDB.value = true
  isButtonClickable.value = true
  isHidden.value = true
  var files = e.target.files
  if (!files.length) {
    return
  }
  folderInput.value = files
}

const uploadFile = async () => {
  resetTimer()
  timerStart()
  isUploading.value = true
  isHidden.value = false
  isUploaded.value = false
  const formData = new FormData()
  console.log(imageInput.value)
  formData.append('image', imageInput.value)
  console.log(formData.get('image'))
  try {
    const response = await axios.post(urlToSend.value, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    console.log(response.data)
    imageData.value = response.data
    isUploaded.value = true
    isUploading.value = false
    stopTimer()
  } catch (error) {
    console.error(error)
    stopTimer()
    isError.value = true
  }
}

const uploadDB = async () => {
  resetTimer()
  timerStart()
  isUploading.value = true
  isHidden.value = false
  isUploaded.value = false
  console.log(folderInput.value)
  const formData = new FormData()
  for (let i = 0; i < folderInput.value.length; i++) {
    formData.append('files', folderInput.value[i])
  }
  console.log(formData.getAll('files'))
  try {
    const response = await axios.post('http://127.0.0.1:5000/uploadDB', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    console.log(formData)
    console.log(response.data)
    isUploading.value = false
    isUploaded.value = true
    stopTimer()
  } catch (error) {
    stopTimer()
    console.error(error)
    isError.value = true
  }
  // }
}

const formattedElapsedTime = computed(() => {
  const date = new Date(null)
  date.setSeconds(elapsedTime.value / 1000)
  const utc = date.toUTCString()
  return utc.substr(utc.indexOf(':') - 2, 8)
})

function timerStart() {
  timer.value = setInterval(() => {
    elapsedTime.value += 1000
  }, 1000)
}

function stopTimer() {
  clearInterval(timer.value)
}

function resetTimer() {
  elapsedTime.value = 0
}
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

.page-item {
  border: 3px solid #ef6e4e;
  padding-top: 0.2em;
  padding-bottom: 0.2em;
  border-radius: 5px;
}

.page-item:hover {
  cursor: pointer;
  color: red;
}
</style>
