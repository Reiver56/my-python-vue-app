<template>
  <div>
    <MonacoEditor @updateCode="code = $event" />
    <button @click="runCode">Run</button>
    <OutputPanel :output="output" />
  </div>
    <Sidebar />
</template>

<script setup>
import MonacoEditor from '@/components/MonacoEditor.vue'
import OutputPanel from '@/components/OutputPanel.vue'
import Sidebar from '@/components/Sidebar.vue'
import { ref } from 'vue'


const code = ref('')
const output = ref('')

async function runCode() {
  const res = await fetch('http://localhost:8000/code/run', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ code: code.value })
  })
  const data = await res.json()
  output.value = data.output
}
</script>

<style scoped>
button {
  margin-top: 1em;
  padding: 0.5em 1em;
}
</style>
