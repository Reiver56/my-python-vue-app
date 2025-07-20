<template>
  <div class="custom-node">
    <textarea
      v-model="localCode"
      @input="updateCode"
      rows="6"
      cols="30"
      placeholder="Inserisci codice..."
    ></textarea>
  </div>
</template>

<script setup>
import { ref, watch, defineEmits, defineProps } from 'vue'

const props = defineProps({
  data: Object,
  id: String
})
const emit = defineEmits(['update:code'])

const localCode = ref(props.data.code || '')

watch(() => props.data.code, (newVal) => {
  if (newVal !== localCode.value) {
    localCode.value = newVal
  }
})

function updateCode() {
  emit('update:code', localCode.value)
}
</script>

<style scoped>
.custom-node {
  border: 1px solid #888;
  padding: 10px;
  background-color: white;
  border-radius: 6px;
  font-family: monospace;
}

textarea {
  width: 100%;
  font-family: monospace;
  font-size: 14px;
  resize: vertical;
}
</style>
