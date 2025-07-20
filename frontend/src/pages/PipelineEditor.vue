<template>
  <div>
    <div class="canvas">
      <VueFlow
        :nodes="nodes"
        :edges="edges"
        :nodeTypes="nodeTypes"
        @nodesChange="onNodesChange"
        @edgesChange="onEdgesChange"
        @nodeDoubleClick="onNodeDoubleClick"
      >
        <template #node-custom="{ id, data }">
          <CustomNode
            :id="id"
            :data="data"
            :selectedNodeId="selectedNodeId"
            @select="selectedNodeId = $event"
            @update:code="code => updateNodeCode(id, code)"
          />
        </template>
      </VueFlow>
    <ModalEditor
        v-if="showEditor"
        :nodeId="editingNodeId"
        :code="editingCode"
        @save="saveCode"
        @close="showEditor = false"
      />
    </div>

    <button @click="runPipeline">Esegui Pipeline</button>
    <button @click="promptAddNode">Aggiungi Nodo</button>
    <button @click="promptAddEdge">Aggiungi Arco</button>

    <div v-if="selectedNodeId">
      <h3>Dettagli Nodo Selezionato: {{ selectedNodeId }}</h3>
      <button @click="promptAddNode">Aggiungi Nodo con Codice</button>
      <button @click="promptAddEdgeFromSelected">Aggiungi Arco da Nodo Selezionato</button>
    </div>
    <MessageBox ref="messageBox" />

    <Sidebar />

    <div class="pipeline-editor">
      <h2>Editor Pipeline</h2>
      <button @click="savePipeline">Salva Pipeline</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { VueFlow } from '@braks/vue-flow'
import '@braks/vue-flow/dist/style.css'
import CustomNode from '@/components/CustomNode.vue'
import Sidebar from '@/components/Sidebar.vue'
import MessageBox from '../components/MessageBox.vue'
import ModalEditor from '../components/ModalEditor.vue'

const showEditor = ref(false)
const editingNodeId = ref(null)
const editingCode = ref('')

const selectedNodeId = ref(null)
const messageBox = ref(null)

const nodeTypes = {
  custom: CustomNode
}

const nodes = ref([
  { id: '1', type: 'custom', position: { x: 100, y: 100 }, data: { code: "print('Nodo 1')" } },
  { id: '2', type: 'custom', position: { x: 300, y: 100 }, data: { code: "print('Nodo 2')" } }
])

const edges = ref([])

let nextNodeId = nodes.value.length + 1

function showMessage(msg, type = 'info') {
  messageBox.value?.show(msg, type)
}

function addEdge(source, target) {
  if (!source || !target) {
    showMessage('Source e target devono essere validi', 'error')
    return
  }
  // Evita duplicati
  if (edges.value.some(e => e.source === source && e.target === target)) {
    showMessage('Arco già esistente', 'error')
    return
  }
  edges.value.push({ id: `${source}-${target}`, source, target })
}

function addNode(code) {
  if (!code) {
    showMessage('Codice nodo non valido', 'error')
    return
  }
  const newNode = {
    id: String(nextNodeId++),
    type: 'custom',
    position: { x: Math.random() * 400, y: Math.random() * 400 },
    data: { code }
  }
  nodes.value.push(newNode)
}

function updateNodeCode(id, newCode) {
  const node = nodes.value.find(n => n.id === id)
  if (node && typeof newCode === 'string') {
    node.data.code = newCode
  }
}

function onEdgesChange(changes) {
  changes.forEach(change => {
    if (change.type === 'remove') {
      edges.value = edges.value.filter(e => e.id !== change.id)
    }
  })
}

function onNodesChange(changes) {
  changes.forEach(change => {
    if (change.type === 'remove') {
      nodes.value = nodes.value.filter(n => n.id !== change.id)
      if (selectedNodeId.value === change.id) {
        selectedNodeId.value = null
      }
    } else {
      const index = nodes.value.findIndex(n => n.id === change.id)
      if (index !== -1) {
        nodes.value[index] = { ...nodes.value[index], ...change }
      }
    }
  })
}

// **Qui la funzione corretta che apre il ModalEditor**
function onNodeDoubleClick({ node }) {
  editingNodeId.value = node.id
  editingCode.value = node.data.code || ''
  showEditor.value = true
}

function saveCode(newCode) {
  updateNodeCode(editingNodeId.value, newCode)
  showEditor.value = false
}

// Prompt per aggiungere nodo
function promptAddNode() {
  const code = prompt('Inserisci codice per il nuovo nodo:')
  if (code) addNode(code)
}

// Prompt per aggiungere arco tra nodi
function promptAddEdge() {
  const source = prompt('Inserisci ID nodo sorgente:')
  const target = prompt('Inserisci ID nodo destinazione:')
  if (source && target) addEdge(source, target)
}

// Aggiunge arco da nodo selezionato a target scelto
function promptAddEdgeFromSelected() {
  if (!selectedNodeId.value) {
    showMessage('Nessun nodo selezionato', 'error')
     return
  }
  const target = prompt('Inserisci ID nodo destinazione:')
  if (target) addEdge(selectedNodeId.value, target)
}

async function savePipeline() {
  const payload = {
    nodes: nodes.value.map(n => ({
      id: n.id,
      code: n.data.code,
      position: n.position,
      next: edges.value.filter(e => e.source === n.id).map(e => e.target)
    }))
  }

  try {
    const res = await fetch('http://localhost:8000/pipeline/save', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    })

    if (!res.ok) throw new Error(`Status: ${res.status}`)

    showMessage('Pipeline salvata con successo', 'success')
    console.log('Pipeline salvata:', payload)
  } catch (e) {
    showMessage('Errore durante il salvataggio: ' + e.message, 'error')
  }
}

async function runPipeline() {
  const payload = {
    nodes: nodes.value.map(n => ({
      id: n.id,
      code: n.data.code,
      next: edges.value.filter(e => e.source === n.id).map(e => e.target)
    }))
  }

  try {
    const res = await fetch('http://localhost:8000/pipeline/run', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    })

    if (!res.ok) throw new Error(`Status: ${res.status}`)

    const data = await res.json()
    showMessage('Pipeline eseguita, nodi eseguiti: ' + data.executed.join(', '))
  } catch (e) {
    showMessage('Errore durante l\'esecuzione: ' + e.message, 'error')
  }
}
</script>

<style scoped>
.canvas {
  border: 1px solid #ccc;
  height: 600px;
  background-color: #f9f9f9;
}

button {
  margin-top: 1em;
  padding: 0.5em 1em;
  background-color: #4CAF50;
  color: white;
  border: none;
  cursor: pointer;
}

button:hover {
  background-color: #45a049;
}

.pipeline-editor {
  padding: 1rem;
}
</style>
