<template>
  <div class="sidebar">
    <ul>
      <li><router-link to="/">Home</router-link></li>
      <li><router-link to="/pipeline">Pipeline</router-link></li>
    </ul>
  </div>
</template>

<script setup>
import { ref } from 'vue'
</script>

<style scoped>
.sidebar {
  width: 200px;
  background-color: #f4f4f4;
  padding: 1em;
}
.sidebar ul {
  list-style-type: none;
  padding: 0;
}
.sidebar li {
  margin: 0.5em 0;
}
</style>