<template>
  <div class="main">
    <MainComponent />
  </div>
</template>

<script>
// @ is an alias to /src
import MainComponent from "@/components/MainComponent.vue";

export default {
  name: "MainPage",
  components: {
    MainComponent,
  },
};
</script>
