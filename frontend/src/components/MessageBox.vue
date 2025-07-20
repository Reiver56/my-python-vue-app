<template>
  <div v-if="visible" :class="['message-box', type]" @click="visible = false">
    {{ message }}
  </div>
</template>

<script setup>
import { ref } from 'vue'

const visible = ref(false)
const message = ref('')
const type = ref('info') // 'success', 'error', 'info'

function show(msg, msgType = 'info', duration = 3000) {
  message.value = msg
  type.value = msgType
  visible.value = true
  setTimeout(() => { visible.value = false }, duration)
}

defineExpose({ show })
</script>

<style scoped>
.message-box {
  position: fixed;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  padding: 12px 20px;
  border-radius: 5px;
  color: white;
  cursor: pointer;
  user-select: none;
  font-weight: bold;
  z-index: 1000;
  transition: opacity 0.3s ease;
}

.message-box.info {
  background-color: #2196f3;
}
.message-box.success {
  background-color: #4caf50;
}
.message-box.error {
  background-color: #f44336;
}
</style>