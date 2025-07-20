<template>
  <div
    class="custom-bridge"
    :class="{ selected: selectedNodeId === id }"
    @click="$emit('select', id)"
  >
    <span>{{ data.label || id }}</span>
  </div>
</template>

<script setup>
defineProps(['id', 'data', 'selectedNodeId'])
defineEmits(['select'])
</script>

<style scoped>
.custom-bridge {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  background: linear-gradient(145deg, #00c6ff, #0072ff);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: bold;
  text-align: center;
  padding: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
  transition: transform 0.2s;
  cursor: pointer;
}
.custom-bridge.selected {
  box-shadow: 0 0 0 4px #ffcc00;
}
</style>
