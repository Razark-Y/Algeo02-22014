<template>
  <div id="Hero" class="flex flex-row flex-wrap justify-around items-center pt-10 mx-10">
    <div id="hugeBait" class="text-8xl font-bold mx-5">
      <span class="text-orange-600">Color</span> <span class="text-lime-600">Based</span><br /><span
        class="text-rose-600"
        >Image</span
      ><br />Retrieval.
    </div>
    <div id="caption" class="w-96 items-center font-normal tracking-wide">
      <div>
        <b>Content-based image retrieval (CBIR)</b> is a powerful technique that allows users to
        search for digital images in large databases based on the contents of the images
        themselves.<br /><br /><b>CBIR</b> analyzes the contents of an image, such as colors,
        shapes, and textures, rather than relying on metadata such as keywords, tags, or
        descriptions associated with the image.
      </div>
      <router-link to="/ImageBased" class="flex">
        <div
          class="bg-indigo-400 rounded-sm px-6 py-2 mt-5 text-white hover:cursor-pointer hover:scale-105"
        >
          Get Started
        </div>
      </router-link>
    </div>
  </div>
</template>

<style scoped>
#hugeBait {
  line-height: 1.1;
}
</style>
