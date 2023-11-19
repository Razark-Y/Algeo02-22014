<template>
  <navigation-bar
    class="glass flex flex-row justify-between py-4 px-[7em] fixed top-0 right-0 left-0 z-50"
  >
    <img src="./assets/logo.svg" height="100" width="200" />
    <div class="flex flex-row gap-8 items-center">
      <router-link
        class-active="active"
        aria-current="page"
        to="/"
        class="font-Merriweather font-bold text-[#ef6e4e] text-[22px] hover:cursor-pointer hover:text-[#e29578]"
        >Home</router-link
      >
      <router-link
        class-active="active"
        to="/CameraBased"
        class="font-Merriweather font-bold text-[#ef6e4e] text-[22px] hover:cursor-pointer"
        >Camera</router-link
      >
      <router-link
        class-active="active"
        to="/About"
        class="font-Merriweather font-bold text-[#ef6e4e] text-[22px] hover:cursor-pointer"
        >About Us</router-link
      >
      <router-link
        class-active="active"
        to="/Scraper"
        class="font-Merriweather font-bold text-[#ef6e4e] text-[22px] hover:cursor-pointer"
        >Web Scraper</router-link
      >
      <router-link
        class-active="active"
        to="/Docs"
        class="font-Merriweather font-bold text-[#ef6e4e] text-[22px] hover:cursor-pointer hover:text-[#e29578]"
        >Docs</router-link
      >
      <router-link
        class-active="active"
        aria-current="page"
        to="/ImageBased"
        class="font-Merriweather font-bold text-[#ef6e4e] text-[22px] hover:cursor-pointer rounded-xl bg-[#97293f] px-6 py-2 hover:bg-[#ffddd2] hover:text-[#792133] transition"
        >Get Started!</router-link
      >
    </div>
  </navigation-bar>
  <div class="bg-[#792133] min-h-screen">
    <router-view class="pb-8"></router-view>
  </div>
</template>

<script setup></script>

<style>
.router-link-active {
  /* color: bisque; */
  color: #792133;
  background-color: #ffddd2;
  padding: 0.3em 1em;
  border-radius: 30px;
}

.glass {
  /* background: rgba(128, 15, 47, 0.2); */
  background: rgba(52, 12, 17, 0.2);
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(9px);
  -webkit-backdrop-filter: blur(5px);
  /* border: 1px solid rgba(255, 255, 255, 0.3); */
}
</style>
