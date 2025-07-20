<template>
  <div class="modal-backdrop" @click.self="close">
    <div class="modal-content">
      <MonacoEditor
        language="python"
        v-model="code"
        height="300"
        theme="vs-dark"
        :options="{ automaticLayout: true }"
      />
      <button @click="save">Salva</button>
      <button @click="close">Annulla</button>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, defineEmits, defineProps } from 'vue'
import MonacoEditor from 'monaco-editor-vue3'

const emit = defineEmits(['save', 'close'])
const props = defineProps({
  modelValue: String
})

const code = ref(props.modelValue)

watch(() => props.modelValue, (val) => {
  code.value = val
})

function save() {
  emit('save', code.value)
}

function close() {
  emit('close')
}
</script>

<style scoped>
.modal-backdrop {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  padding: 1rem;
  border-radius: 6px;
  width: 600px;
  max-width: 90vw;
}
</style>
