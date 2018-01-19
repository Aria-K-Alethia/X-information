<template>
  <div id="app">
    <router-view></router-view>
    <Footer></Footer>
  </div>
  
</template>

<script>
import Footer from './components/general/Footer.vue'
export default {
  name: 'app',
  components: { Footer }
}
</script>

<style>
</style>
