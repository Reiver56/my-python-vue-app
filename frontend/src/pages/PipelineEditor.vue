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
        </template>
      </VueFlow>
    </div>

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
      <!-- Aggiungiamo il bottone per salvare il singolo nodo -->
      <button v-if="editingNodeId" @click="saveNode(editingNodeId)">Salva Nodo</button>
    </div>

    <MessageBox ref="messageBox" />
    <Sidebar />

    <div class="pipeline-editor">
      <button @click="savePipeline">Salva Pipeline</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { VueFlow } from '@braks/vue-flow'
import CustomNode from '@/components/CustomNode.vue'
import ModalEditor from '@/components/ModalEditor.vue'
import MessageBox from '@/components/MessageBox.vue'
import Sidebar from '@/components/Sidebar.vue'

const nodes = ref([])
const edges = ref([])
let nextNodeId = 1
const nodeTypes = { custom: CustomNode }
const messageBox = ref(null)

const showEditor = ref(false)
const editingNodeId = ref(null)
const editingCode = ref('')

function showMessage(msg, type='info') {
  messageBox.value?.show(msg, type)
}

function onNodeDoubleClick({ node }) {
  editingNodeId.value = node.id
  editingCode.value = node.data.code || ''
  showEditor.value = true
}

function saveCode(newCode) {
  const n = nodes.value.find(n => n.id === editingNodeId.value)
  if (n) n.data.code = newCode
  showEditor.value = false
}

function updateNodeCode(id, newCode) {
  const n = nodes.value.find(n => n.id === id)
  if (n) n.data.code = newCode
}

function onNodesChange(ch) {
  ch.forEach(c => {
    if (c.type==='remove') nodes.value = nodes.value.filter(n=>n.id!==c.id)
    else {
      const i=nodes.value.findIndex(n=>n.id===c.id)
      if(i!==-1) nodes.value[i]={...nodes.value[i],...c}
    }
  })
}

function onEdgesChange(ch) {
  ch.forEach(c=>{
    if(c.type==='remove') edges.value=edges.value.filter(e=>e.id!==c.id)
  })
}

function promptAddNode() {
  const code = prompt('Codice del nuovo nodo:')
  if(!code) return showMessage('Codice vuoto','error')
  const id=String(nextNodeId++)
  nodes.value.push({id,type:'custom',position:{x:Math.random()*400,y:Math.random()*400},data:{code}})
  showMessage(`Nodo ${id} aggiunto`,'success')
}

function promptAddEdge() {
  const s=prompt('ID sorgente:'),t=prompt('ID destinazione:')
  if(!s||!t) return showMessage('ID mancanti','error')
  if(edges.value.some(e=>e.source===s&&e.target===t)) return showMessage('Arco già esistente','error')
  edges.value.push({id:`${s}-${t}`,source:s,target:t})
  showMessage(`Arco ${s}->${t} aggiunto`,'success')
}

async function savePipeline() {
  const payload={nodes:nodes.value.map(n=>({id:n.id,code:n.data.code,next:edges.value.filter(e=>e.source===n.id).map(e=>e.target)}))}
  try{
    const res=await fetch('http://localhost:8000/pipeline/save',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)})
    if(!res.ok) throw new Error(await res.text())
    showMessage('Pipeline salvata','success')
  }catch(e){showMessage(`Errore salvataggio: ${e.message}`,'error')}
}

async function runPipeline() {
  const payload={nodes:nodes.value.map(n=>({id:n.id,code:n.data.code,next:edges.value.filter(e=>e.source===n.id).map(e=>e.target)}))}
  try{
    const res=await fetch('http://localhost:8000/pipeline/run',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)})
    if(!res.ok) throw new Error(await res.text())
    const data=await res.json()
    showMessage(`Eseguiti: ${data.executed.join(', ')}`,'success')
  }catch(e){showMessage(`Errore esecuzione: ${e.message}`,'error')}
}

async function saveNode(id) {
  const n=nodes.value.find(n=>n.id===id)
  if(!n) return showMessage('Nodo non trovato','error')
  console.log(n.id)
  try{
    const res=await fetch(`http://localhost:8000/pipeline/${n.id}/savenode`,{
      method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(n.data.code)
    })
    if(!res.ok) throw new Error(await res.text())
    showMessage(`Nodo ${id} salvato`,'success')
  }catch(e){showMessage(`Errore salvataggio nodo: ${e.message}`,'error')}
}
</script>

<style scoped>
.canvas{border:1px solid #ccc;height:600px;background:#f9f9f9}
.controls{margin:1rem 0;display:flex;gap:1rem}
.pipeline-editor{padding:1rem}
button{padding:.5em 1em;background:#4CAF50;color:#fff;border:none;cursor:pointer}
button:hover{background:#45a049}
</style>