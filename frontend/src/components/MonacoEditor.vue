<template>
  <div ref="editorContainer" class="editor-container"></div>
</template>

<script setup>
import * as monaco from 'monaco-editor'
import { ref, onMounted } from 'vue'

const editorContainer = ref(null)
const emit = defineEmits(['updateCode'])
let editor

onMounted(() => {
  editor = monaco.editor.create(editorContainer.value, {
    value: '# Write your Python code here',
    language: 'python',
    theme: 'vs-dark',
    automaticLayout: true,
  })

  editor.onDidChangeModelContent(() => {
    emit('updateCode', editor.getValue())
  })
})
</script>

<style scoped>
.editor-container {
  height: 400px;
  width: 100%;
}
</style>
