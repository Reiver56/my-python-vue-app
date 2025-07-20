<!-- src/components/ModalEditor.vue -->
<template>
  <div class="modal-backdrop" @click.self="close">
    <div class="modal-content">
      <MonacoEditor
        v-model:value="code"           
        language="python"
        theme="vs-dark"
        :options="{ automaticLayout: true }"
      />
      <div class="modal-footer">
        <button @click="onSave">Salva</button>
        <button @click="onClose">Annulla</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, defineProps, defineEmits } from 'vue'
import MonacoEditor from 'monaco-editor-vue3'  // o il wrapper che stai usando

const props = defineProps({
  code: { type: String, required: true }
})
const emit = defineEmits(['save','close'])

const code = ref(props.code)

// Sincronizza se cambia la prop
watch(() => props.code, val => (code.value = val))

function onSave() {
  emit('save', code.value)   // <-- deve chiamarsi proprio 'save'
}
function onClose() {
  emit('close')
}
</script>

<style scoped>
.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
    backdrop-filter: blur(5px);
    cursor: pointer;
    transition: opacity 0.3s ease;
    opacity: 0.8;
    pointer-events: none;
    pointer-events: auto;
}

.modal-content {
  background: white;
  padding: 1rem;
  border-radius: 6px;
  width: 600px;
  max-width: 90vw;
    position: relative;
    cursor: default;
    display: flex;
    flex-direction: column;
    gap: 1rem;
    font-family: monospace;
    height: 400px;
}
.modal-footer {
  display: flex;
  justify-content: flex-end;
  margin-top: 1rem;
}
button {
  margin-left: 0.5rem;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  background-color: #007bff;
  color: white;
  cursor: pointer;
}
button:hover {
  background-color: #0056b3;
}
</style>
