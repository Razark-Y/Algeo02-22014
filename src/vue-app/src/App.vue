<template>
  <navigation-bar
    class="bg-purple-800 flex flex-row justify-around py-4 fixed top-0 right-0 left-0 z-50"
  >
    <img src="./assets/logo.svg" height="100" width="200" />
    <div class="flex flex-row gap-4 items-center">
      <router-link
        class-active="active"
        aria-current="page"
        to="/"
        class="font-bold text-gray-100 hover:cursor-pointer"
        >Home</router-link
      >
      <router-link
        class-active="active"
        aria-current="page"
        to="/ImageBased"
        class="font-bold text-gray-100 hover:cursor-pointer"
        >Image</router-link
      >
      <router-link
        class-active="active"
        to="/CameraBased"
        class="font-bold text-gray-100 hover:cursor-pointer"
        >Camera</router-link
      >
      <router-link
        class-active="active"
        to="/About"
        class="font-bold text-gray-100 hover:cursor-pointer"
        >About Us</router-link
      >
      <router-link
        class-active="active"
        to="/Scraper"
        class="font-bold text-gray-100 hover:cursor-pointer"
        >Web Scraper</router-link
      >
      <router-link
        class-active="active"
        to="/Docs"
        class="font-bold text-gray-100 hover:cursor-pointer"
        >Docs</router-link
      >
    </div>
  </navigation-bar>
  <router-view class="mt-20"></router-view>
</template>

<script setup></script>

<style>
.router-link-active {
  color: bisque;
}
</style>
