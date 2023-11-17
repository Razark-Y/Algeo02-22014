<template>
  <div>
    <video ref="video" autoplay playsinline webkit-playsinline muted hidden></video>
    <canvas ref="canvas" width="300" height="200" class="bg-black rounded-3xl"></canvas>

    <button @click.prevent="TakePicture" class="p-4 bg-slate-500">Take Picture</button>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

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
    .post('http://127.0.0.1:5000/uploadColorCamera', { file: imageBase64 })
    .then((response) => {
      console.log(response)
    })
    .catch((error) => {
      console.log(error)
    })

  // const formData = new FormData();
  // // console.log(imageBase64);
  // formData.append('image', imageBase64);
  // console.log(formData.get('image'))
  // try{
  //   const response = await axios.post('http://127.0.0.1:5000/uploadColorCamera', formData, {
  //     headers: {
  //       'Content-Type': 'multipart/form-data'
  //     }
  //   })
  //   console.log(response.data);
  // } catch(error) {
  //   console.error(error);
  // }
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
</script>
