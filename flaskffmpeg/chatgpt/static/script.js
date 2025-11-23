// script.js

// --- GLOBAL STATE ---
let editor;                // instance Drawflow
let currentSelectedNodeId; // node id actuellement sélectionné
let currentUploadedVideoPath = null; // chemin back de la vidéo uploadée

document.addEventListener("DOMContentLoaded", () => {
  initEditor();
  initPalette();
  initUpload();
  initButtons();
});

/////////////////////////////////////////////
// Init Drawflow
/////////////////////////////////////////////
function initEditor() {
  const container = document.getElementById('drawflow');
  editor = new Drawflow(container);
  editor.reroute = true;
  editor.start();

  // autoriser le drag déplacable dans l'éditeur
  container.addEventListener('drop', dropNode);
  container.addEventListener('dragover', allowDrop);

  // écoute sélection de node
  editor.on('nodeSelected', (id) => {
    currentSelectedNodeId = id;
    renderInspectorForNode(id);
  });

  editor.on('nodeDataChanged', (id) => {
    // si on change les inputs dans l'inspector,
    // on peut re-render pour rester sync
    if (currentSelectedNodeId === id) {
      renderInspectorForNode(id);
    }
  });

  // créer un node Output de base (optionnel)
  const outputHtml = `
    <div class="node-block">
      <div class="title">Output</div>
      <p>Rendu final MP4</p>
    </div>`;
  const outId = editor.addNode(
    'output',
    1, // inputs
    0, // outputs
    700, // pos x
    200, // pos y
    'output',
    {},
    outputHtml
  );

  // tu peux créer un node Input vide aussi, l’utilisateur peut ensuite lui assigner la vidéo uploadée
  const inputHtml = `
    <div class="node-block">
      <div class="title">Input Video</div>
      <p id="input-path-label">No file</p>
    </div>`;
 /*
  const inId = editor.addNode(
    'input',
    0,
    1,
    100,
    200,
    'input',
    { path: null },
    inputHtml
  ); */
}


/////////////////////////////////////////////
// Palette de nodes (sidebar -> éditeur)
/////////////////////////////////////////////
function initPalette() {
  document.querySelectorAll('.node-btn').forEach(btn => {
    btn.setAttribute('draggable', true);
    btn.addEventListener('dragstart', dragNodeStart);
  });
}

function dragNodeStart(ev) {
  ev.dataTransfer.setData("node", ev.target.getAttribute("data-node"));
}

function allowDrop(ev) {
  ev.preventDefault();
}

function dropNode(ev) {
  ev.preventDefault();
  const nodeType = ev.dataTransfer.getData("node");
  addNodeAtPosition(nodeType, ev.clientX, ev.clientY);
}

// helper pour placer un node
function getOffset(el) {
  const rect = el.getBoundingClientRect();
  return { left: rect.left + window.scrollX, top: rect.top + window.scrollY };
}

function addNodeAtPosition(type, x, y) {
  const container = document.getElementById('drawflow');
  const zoom = editor.zoom;
  const offset = getOffset(container);

  const pos_x = (x - offset.left) / zoom;
  const pos_y = (y - offset.top) / zoom;

  let html = '';
  let inputs = 1;
  let outputs = 1;
  let data = {};

  switch (type) {
    case 'input':
      inputs = 0;
      outputs = 1;
      data = { path: currentUploadedVideoPath };
      html = `
        <div class="node-block">
          <div class="title">Input Video</div>
          <p>${currentUploadedVideoPath || 'No file'}</p>
        </div>`;
      break;

    case 'brightness':
      data = { brightness: 0.0, contrast: 1.0, saturation: 1.0 };
      html = `
        <div class="node-block">
          <div class="title">Brightness / Contrast</div>
          <p>eq filter</p>
        </div>`;
      break;

    case 'crop':
      data = { w: 640, h: 360, x: 0, y: 0 };
      html = `
        <div class="node-block">
          <div class="title">Crop</div>
          <p>cut frame</p>
        </div>`;
      break;

    case 'grayscale':
      data = {};
      html = `
        <div class="node-block">
          <div class="title">Grayscale</div>
          <p>format=gray</p>
        </div>`;
      break;

    case 'scale':
      data = { width: 640, height: 360 };
      html = `
        <div class="node-block">
          <div class="title">Scale</div>
          <p>resize</p>
        </div>`;
      break;

    case 'output':
      inputs = 1;
      outputs = 0;
      data = {};
      html = `
        <div class="node-block">
          <div class="title">Output</div>
          <p>Rendu final MP4</p>
        </div>`;
      break;

    default:
      console.warn("Type de node inconnu:", type);
      return;
  }

  editor.addNode(type, inputs, outputs, pos_x, pos_y, type, data, html);
}


/////////////////////////////////////////////
// Inspector (panneau de droite)
/////////////////////////////////////////////
function renderInspectorForNode(id) {
  const inspector = document.getElementById('inspector');
  const node = editor.getNodeFromId(id);

  if (!node) {
    inspector.innerHTML = `<div class="no-selection">Sélectionne un node…</div>`;
    return;
  }

  let html = `<div><strong>${node.name}</strong></div>`;

  // champs dynamiques selon le type
  if (node.name === 'input') {
    html += `
      <label>Chemin / Upload</label>
      <input type="text" data-field="path" value="${node.data.path || ''}">
      <small style="color:#888;">(Défini après upload)</small>
    `;
  }

  if (node.name === 'brightness') {
    html += `
      <label>Brightness (-1.0 à 1.0)</label>
      <input type="number" step="0.1" data-field="brightness" value="${node.data.brightness}">
      <label>Contrast (>0)</label>
      <input type="number" step="0.1" data-field="contrast" value="${node.data.contrast}">
      <label>Saturation (>0)</label>
      <input type="number" step="0.1" data-field="saturation" value="${node.data.saturation}">
    `;
  }

  if (node.name === 'crop') {
    html += `
      <label>Width</label>
      <input type="number" data-field="w" value="${node.data.w}">
      <label>Height</label>
      <input type="number" data-field="h" value="${node.data.h}">
      <label>X</label>
      <input type="number" data-field="x" value="${node.data.x}">
      <label>Y</label>
      <input type="number" data-field="y" value="${node.data.y}">
    `;
  }

  if (node.name === 'scale') {
    html += `
      <label>Width</label>
      <input type="number" data-field="width" value="${node.data.width}">
      <label>Height</label>
      <input type="number" data-field="height" value="${node.data.height}">
    `;
  }

  if (node.name === 'grayscale') {
    html += `
      <p>No options.</p>
    `;
  }

  if (node.name === 'output') {
    html += `<p>Sortie finale MP4</p>`;
  }

  inspector.innerHTML = html;

  // brancher les inputs -> update node.data
  inspector.querySelectorAll('input[data-field]').forEach(inputEl => {
    inputEl.addEventListener('input', (e) => {
      const field = e.target.getAttribute('data-field');
      const value = e.target.value;
      node.data[field] = tryNumber(value);
      editor.updateNodeDataFromId(id, node.data);
    });
  });
}

function tryNumber(v) {
  if (v === '' || isNaN(v)) return v;
  return Number(v);
}


/////////////////////////////////////////////
// Upload vidéo -> POST /upload
/////////////////////////////////////////////
function initUpload() {
  const fileInput = document.getElementById('video-input');
  fileInput.addEventListener('change', async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('video', file);

    const res = await fetch('/upload', {
      method: 'POST',
      body: formData
    });

    const json = await res.json();
    if (json.status === "ok") {
      currentUploadedVideoPath = json.path;
      alert("Upload OK !");
      // mettre à jour tous les nodes input existants
      Object.keys(editor.drawflow.drawflow.Home.data).forEach(id => {
        const n = editor.getNodeFromId(id);
        if (n.name === 'input') {
          n.data.path = currentUploadedVideoPath;
          editor.updateNodeDataFromId(id, n.data);
        }
      });
    } else {
      alert("Erreur upload: " + json.error);
    }
  });
}


/////////////////////////////////////////////
// Générer Preview / Export complet
/////////////////////////////////////////////
function initButtons() {
  document.getElementById('btn-preview').addEventListener('click', async () => {
    const g = serializeGraph();
    const res = await fetch('/process', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(g)
    });
    const json = await res.json();
    if (json.status === 'ok') {
      setPreviewVideo(json.url);
    } else {
      alert("Erreur preview: " + json.error);
    }
  });

  document.getElementById('btn-render').addEventListener('click', async () => {
    const g = serializeGraph();
    const res = await fetch('/render_full', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(g)
    });
    const json = await res.json();
    if (json.status === 'ok') {
      setPreviewVideo(json.url);
      alert("Export complet prêt !");
    } else {
      alert("Erreur export: " + json.error);
    }
  });
}

function setPreviewVideo(url) {
  const videoEl = document.getElementById('preview-video');
  videoEl.src = url;
  videoEl.load();
  videoEl.play().catch(() => {});
}


/////////////////////////////////////////////
// Sérialiser le graph Drawflow pour l'envoyer au backend
/////////////////////////////////////////////
function serializeGraph() {
  // On part du principe que tout est dans 'Home'
  // drawflow structure: editor.drawflow.drawflow.Home.data
  const data = editor.drawflow.drawflow.Home.data;

  // On va transformer en structure légère que le backend attend
  // {
  //   nodes: {
  //     "1": {
  //        name: "input",
  //        data: {...},
  //        outputs: { out: [ {node:"2", input:"in"} ] }
  //     },
  //     ...
  //   }
  // }

  const result = { nodes: {} };

  Object.keys(data).forEach(id => {
    const node = data[id];

    // Les connexions sortantes
    // Drawflow stocke dans node.outputs[<port>].connections = [ { node:'X', input:'Y'} ...]
    const outs = {};
    Object.keys(node.outputs).forEach(port => {
      outs[port] = node.outputs[port].connections.map(c => ({
        node: c.node,
        input: c.input
      }));
    });

    result.nodes[id] = {
      name: node.name,
      data: node.data,
      outputs: outs
    };
  });

  return result;
}

