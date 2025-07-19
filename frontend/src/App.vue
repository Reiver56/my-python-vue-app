<template>
  <main>
    <h1>NodePython</h1>
    <textarea v-model="code" rows="10" cols="50"></textarea>
    <br />
    <button @click="runCode">Execute</button>
    <pre>{{ output }}</pre>
  </main>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const code = ref(`print("Ciao dal backend!")`)
const output = ref('')

async function runCode() {
  try {
    const res = await axios.post('http://localhost:8000/run', { code: code.value })
    output.value = res.data.output
  } catch (err) {
    output.value = 'Errore: ' + (err.response?.data?.detail || err.message)
  }
}
</script>

<style>
main {
  padding: 2rem;
  font-family: sans-serif;
}
textarea {
  width: 100%;
  font-family: monospace;
}
pre {
  background-color: #0c0909ff;
  padding: 1rem;
  white-space: pre-wrap;
}
</style>
