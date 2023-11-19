<template>
  <div class="bg-[#792133] w-[100%] h-[100%] pt-[85px] pb-[40px]">
    <div class="Start-Container pl-[60px] bg-[#ffddd2] pb-[30px]">
      <h1 className=" text-[#792133] font-Merriweather text-[40px] font-black ">User Guides</h1>
      <div
        class="Text-Choice flex flex-col justify-evenly text-[#EF6E4E] font-Merriweather text-[28px] font-black ml-[70px]"
      >
        <a
          href="#section1"
          class="py-1 hover:bg-[#792133] w-[650px] pl-[15px] rounded-[30px] transition"
          >Manual User Input Reverse Image Search</a
        >
        <a
          href="#section2"
          class="py-1 hover:bg-[#792133] w-[650px] pl-[15px] rounded-[30px] transition"
          >Web Scrapping Reverse Image Search</a
        >
        <a
          href="#section3"
          class="py-1 hover:bg-[#792133] w-[650px] pl-[15px] rounded-[30px] transition"
          >Camera Input Reverse Image Search</a
        >
      </div>
      <div class="Tools-Block">
        <h1 className="text-[#792133] font-Merriweather text-[40px] font-black">
          Programming Languages
        </h1>
        <div class="Image-Block flex justify-center my-[30px]">
          <a href="https://docs.python.org/3/" target="_blank">
            <img
              src="../assets/img/python.png"
              alt="python"
              className=" rounded-[40px] mx-[10px] w-[200px] h-[200px]"
            />
          </a>
          <a href="https://tailwindcss.com/docs/installation" target="_blank">
            <img
              src="../assets/img/Tailwind.png"
              alt="Tailwind"
              className=" rounded-[40px] mx-[10px] w-[300px] h-[200px]"
            />
          </a>
          <a href="https://flask.palletsprojects.com/en/3.0.x/" target="_blank">
            <img
              src="../assets/img/Flask.png"
              alt="Tailwind"
              className=" rounded-[40px] mx-[10px] w-[300px] h-[200px]"
            />
          </a>
        </div>
      </div>
    </div>
    <div class="Manual-Container mx-[60px] my-[30px] pb-[40px]">
      <p class="text-[#EF6E4E] font-Merriweather text-[40px] font-black mb-[20px]">
        Content-Based Image Retrieval
      </p>
      <p class="text-[#ffddd2] font-Merriweather text-[28px] font-black">
        Content-Based Image Retrieval (CBIR) is a technology at the forefront of digital image
        search and retrieval. Unlike traditional methods that rely on textual annotations or
        keywords to find images, CBIR uses the actual content of the images to conduct the search.
        This "content" refers to various visual features of the image such as color, texture, shape,
        and spatial layout.
      </p>
    </div>
    <div class="Manual-input mx-[60px] my-[50px] pb-[40px]" id="section1">
      <h1 class="text-[#EF6E4E] font-Merriweather text-[40px] font-black mb-[20px]">
        Manual User Input Image Search
      </h1>
      <div class="Steps text-[#ffddd2] font-Merriweather text-[32px] font-black mb-[20px]">
        <p>1. Select the image you want to search in the image-box</p>
        <p>
          2. Press input dataset and select the dataset you want to upload, then press upload
          dataset
        </p>
        <p>3. Pick your search preference (color/teksture)</p>
        <p>4. Press the search button and wait patiently</p>
        <p>5. Set of images with high similarity will show in a minute</p>
        <p>
          6. If you would like to use another dataset, press the input dataset button and enter a
          new one
        </p>
        <p>7. After inputing a new dataset, page will refresh, meaning dataset is uploaded</p>
        <p>8. Now repeat the process to find high similarity images</p>
      </div>
    </div>
    <div class="Second-Set bg-[#ffddd2] pt-[30px]" id="section2">
      <div class="Manual-input mx-[60px] my-[30px] pb-[40px]">
        <h1 class="text-[#EF6E4E] font-Merriweather text-[40px] font-black mb-[20px]">
          Web Scrapping Reverse Image Search
        </h1>
        <div class="Steps text-[#792133] font-Merriweather text-[32px] font-black mb-[20px]">
          <p>1. Enter the website link you would like to make as your datasets</p>
          <p>2. Select the image you want to search in the image-box</p>
          <p>3. Press the Scrap it! button and wait patiently</p>
          <p>
            4. Press the Search button and wait patiently, you can also choose your preference
            (color/teksture)
          </p>
          <p>5. Set of images with high similarity will show in a minute</p>
          <p>
            6. If you would like to use another dataset, enter a new website link and repeat the
            process
          </p>
        </div>
      </div>
      <div class="Manual-input mx-[60px] my-[30px] pb-[40px]">
        <h1 class="text-[#EF6E4E] font-Merriweather text-[40px] font-black mb-[20px]">
          Camera Input Reverse Image Search
        </h1>
        <div class="Steps text-[#792133] font-Merriweather text-[32px] font-black mb-[20px]">
          <p>1. Make sure your device is connected with a webcam</p>
          <p>
            2. Press input dataset and select the dataset you want to upload, then press upload
            dataset
          </p>
          <p id="section3">3. Pick your search preference (color/teksture)</p>
          <p>4. Wait patiently as the camera will consistently take picture of you</p>
          <p>5. Set of images with high similarity will show over time</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'YourComponentName', // Replace with your component's name

  mounted() {
    this.addSmoothScrolling()
  },

  methods: {
    addSmoothScrolling() {
      document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
        anchor.addEventListener('click', function (e) {
          e.preventDefault()
          const target = document.querySelector(this.getAttribute('href'))
          if (target) {
            target.scrollIntoView({ behavior: 'smooth' })
          }
        })
      })
    }
  }
}
</script>
