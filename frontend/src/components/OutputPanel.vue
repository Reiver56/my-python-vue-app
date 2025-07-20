<template>
  <pre class="output">{{ output }}</pre>
</template>

<script setup>
defineProps({ output: String })
</script>

<style scoped>
.output {
  background-color: #222;
  color: #0f0;
  padding: 1em;
  margin-top: 1em;
  white-space: pre-wrap;
}
</style>
