<template >
  <div id="background" class="bg-[#792133] min-h-screen">
    <div class="flex flex-col justify-center items-center gap-8 mb-4 pt-[8rem]">
      <div class="flex gap-5">
        <div class="overflow-clip">
          <video ref="video" autoplay playsinline webkit-playsinline muted hidden></video>
          <canvas ref="canvas" width="300" height="200" class="bg-black rounded-3xl"></canvas>
        </div>
        <div>
          <form method="POST" enctype="multipart/form-data">
            <div class="flex flex-col items-center">
              <div class="flex flex-col justify-end mb-3"></div>
            </div>
          </form>
        </div>
      </div>
  
      <div id="addDatabase">
        <form method="POST" enctype="multipart/form-data">
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
            <label for="toogleButton" class="flex flex-col gap-1 items-center cursor-pointer">
              <div v-if="!tipeInput" class="px-2 font-thin">Color</div>
              <div v-else class="px-2 font-thin">Texture</div>
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
  </div>
</template>

<script setup>
import Paginate from 'vuejs-paginate-next'
// import Gambar from '../components/gambar-viewer.vue'
import axios from 'axios'
// import Camera from '../components/Camera-Feed.vue'
import { ref, computed, onMounted } from 'vue'
//   import type { InstanceType } from 'vue'

// STATE
const isError = ref(false)
const isUploading = ref(false)
const isButtonClickable = ref(false)
const isHidden = ref(true)
const isUploaded = ref(false)
const currentPage = ref(0)
const tipeInput = ref(false)
const urlToSend = ref('http://127.0.0.1:5000/uploadColorCamera')
const isDB = ref(false)
const isINPT = ref(false)

// DATA
const folderInput = ref([])
const imageData = ref([])

function changeUrl() {
  if (tipeInput.value === true) {
    urlToSend.value = 'http://127.0.0.1:5000/uploadColorCamera'
  } else {
    urlToSend.value = 'http://127.0.0.1:5000/uploadTextureCamera'
  }
}

function changePage(value) {
  console.log(value)
  currentPage.value = parseInt(value) - 1
}

const sortedImageData = computed(() => {
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
  if ((subData.length != 0) && inLoop) {
    data.push(subData)
  }
  return data
})

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

const uploadDB = async () => {
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
    isUploaded.value = true
  } catch (error) {
    console.error(error)
    isError.value = true
  }
  // }
  isUploading.value = false
}

const canvas = ref(null)
const video = ref(null)
const ctx = ref(null)

const constraints = ref({
  audio: false,
  video: { width: 300, height: 200 }
})

function SetStream(stream) {
  video.value.srcObject = stream
  video.value.play()

  requestAnimationFrame(Draw)
}

function Draw() {
  ctx.value.drawImage(video.value, 0, 0, canvas.value.width, canvas.value.height)

  requestAnimationFrame(Draw)
}

const TakePicture = async () => {
  // Convert the base64 string to binary data
  const imageBase64 = canvas.value.toDataURL()
  const base64 = imageBase64.split(',')[1]
  console.log(base64)
  // Send the FormData object to the Flask endpoint with Axios
  axios
    .post(urlToSend.value, { file: imageBase64 })
    .then((response) => {
      imageData.value = response.data
      console.log(response.data)
    })
    .catch((error) => {
      console.log(error)
    })
}

onMounted(async () => {
  if (video.value && canvas.value) {
    ctx.value = canvas.value.getContext('2d')

    await navigator.mediaDevices
      .getUserMedia(constraints.value)
      .then(SetStream)
      .catch((e) => {
        console.error(e)
      })
  }
})

onMounted(() => {
  console.log('KIRIM')
  setInterval(TakePicture, 3000)
})
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
  border: 1px solid blueviolet;
  padding-top: 0.2em;
  padding-bottom: 0.2em;
  border-radius: 5px;
}

.page-item:hover {
  cursor: pointer;
  color: salmon;
}
</style>
