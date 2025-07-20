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
            @update:code="code => updateNodeCode(id, code)"
          />
          <CustomBridge :source="id" :target="data.target" />
        </template>
      </VueFlow>
    </div>

    <!-- Modal per edit del codice -->
    <ModalEditor
      v-if="showEditor"
      :code="editingCode"
      @save="saveCode"
      @close="showEditor = false"
    />

    <div class="controls">
      <button @click="runPipeline">Esegui Pipeline</button>
      <button @click="promptAddNode">Aggiungi Nodo</button>
      <button @click="promptAddEdge">Aggiungi Arco</button>
    </div>

    <MessageBox ref="messageBox" />
    <Sidebar />

    <div class="pipeline-editor">
      <h2>Editor Pipeline</h2>
      <button @click="savePipeline">Salva Pipeline</button>
      <button @click="promptAddNode">Aggiungi Nodo</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { VueFlow } from '@braks/vue-flow'
import '@braks/vue-flow/dist/style.css'
import CustomNode from '@/components/CustomNode.vue'
import Sidebar from '@/components/Sidebar.vue'
import MessageBox from '@/components/MessageBox.vue'
import ModalEditor from '@/components/ModalEditor.vue'  // verifica percorso
import CustomBridge  from '../components/CustomBridge.vue'

// ——————————————
// Stato del modal e nodo in modifica
const showEditor = ref(false)
const editingNodeId = ref(null)
const editingCode = ref('')

// Stato principale
const nodes = ref([
  { id: 'ex1', type: 'custom', position: { x: 100, y: 100 }, data: { code: "print('ex1')" } },
  { id: 'ex2', type: 'custom', position: { x: 500, y: 100 }, data: { code: "print('ex2')" } }
])
const edges = ref([])
let nextNodeId = nodes.value.length + 1

const nodeTypes = { custom: CustomNode }
const onNodesChange = (changes) => {
  nodes.value = VueFlow.applyNodeChanges(changes, nodes.value)
}
const onEdgesChange = (changes) => {
  edges.value = VueFlow.applyEdgeChanges(changes, edges.value)
}
// ——————————————
const messageBox = ref(null)
function showMessage(msg, type='info') {
  messageBox.value?.show(msg, type)
}

// ——————————————
// Apri il modal al doppio click
function onNodeDoubleClick({ node }) {
  console.log(node.data.code)
  editingNodeId.value = node.id
  editingCode.value = node.data.code || ''
  showEditor.value = true
}

// Salva il codice modificato dal modal
function saveCode(newCode) {
  const node = nodes.value.find(n => n.id === editingNodeId.value)
  if (node) {
    node.data.code = newCode
    showMessage(`Codice per nodo ${node.id} aggiornato`, 'success')
  }
  console.log(`Salvato codice per nodo ${node.id}:`, newCode)
  showEditor.value = false
}

// Edit inline da CustomNode
function updateNodeCode(id, newCode) {
  const node = nodes.value.find(n => n.id === id)
  if (node) node.data.code = newCode
}

// salva la pipeline su file
async function savePipeline() {
    console.log('Salvataggio pipeline...')
    console.log('Nodes:', nodes.value)
    console.log('Edges:', edges.value)
    if (nodes.value.length === 0) {
      showMessage('Nessun nodo da salvare', 'error')
      return
    }
    if (edges.value.length === 0) {
      showMessage('Nessun arco da salvare', 'error')
      return
    }
  try {
    const response = await fetch('http://localhost:8000/pipeline/save', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ nodes: nodes.value, edges: edges.value })
    })
    if (!response.ok) throw new Error('Errore nel salvataggio della pipeline')
    const data = await response.json()
    showMessage(data.message, 'success')
  } catch (error) {
    showMessage(`Errore: ${error.message}`, 'error')
  }
}

// ——————————————
// Aggiungi un nodo personalizzato
function promptAddNode() {
  const code = prompt('Inserisci codice per il nuovo nodo:', 'print("Nuovo Nodo")')
  if (code) {
    const newNode = {
      id: `node-${nextNodeId++}`,
      type: 'custom',
      position: { x: Math.random() * 800, y: Math.random() * 600 },
      data: { code }
    }
    nodes.value.push(newNode)
    showMessage(`Nodo ${newNode.id} aggiunto`, 'success')
  }
}
// ——————————————
// Aggiungi un arco tra due nodi
function promptAddEdge() {
    const fromNodeId = prompt('Inserisci ID nodo di partenza:')
    const toNodeId = prompt('Inserisci ID nodo di arrivo:')
    if (fromNodeId && toNodeId) {
        const newEdge = {
        id: `edge-${fromNodeId}-${toNodeId}`,
        source: fromNodeId,
        target: toNodeId
        }
        edges.value.push(newEdge)
        showMessage(`Arco da ${fromNodeId} a ${toNodeId} aggiunto`, 'success')
    }
}


// Resto delle funzioni (aggiungi/rimuovi, save/run pipeline…)

</script>

<style scoped>
.canvas { border:1px solid #ccc; height:600px; background:#f9f9f9 }
.controls { margin:1rem 0; display:flex; gap:1rem }
.pipeline-editor { padding:1rem }
button { padding:0.5em 1em; background:#4CAF50; color:#fff; border:none; cursor:pointer }
button:hover { background:#45a049 }
</style>
