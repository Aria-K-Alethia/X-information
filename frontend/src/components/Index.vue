<template>
  <div>
    <Header></Header>
    <Notification></Notification>
  </div>
</template>

<script type="text/javascript">
// import $ from 'jquery'
import Header from './general/Header.vue'
// import Footer from './general/Footer.vue'
import Notification from './Notification/Notification.vue'
export default{
  name: 'Index',
  components: {
    Header,
    Notification
  }
}
</script>

<style type="text/css" scoped>
  
</style>