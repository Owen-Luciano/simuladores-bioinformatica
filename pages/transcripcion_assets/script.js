/* =========================================================================
   SIMULADOR DE TRANSCRIPCIÓN Y TRADUCCIÓN DEL ADN
   -------------------------------------------------------------------------
   Estructura del archivo:
   1. Datos científicos base (complementariedad, tabla del código genético)
   2. Funciones puras del núcleo computacional (transcribe, traducir)
   3. Casos de validación (comparables con herramientas reales)
   4. Lógica de interfaz (pestañas, ayuda guiada, barra de progreso)
   5. Animaciones paso a paso (transcripción y traducción)
   6. Autoevaluación
   ========================================================================= */

/* -------------------------------------------------------------------------
   1. DATOS CIENTÍFICOS BASE
   ------------------------------------------------------------------------- */

// Complementariedad de bases para transcripción ADN -> ARNm.
// Regla real: A-T y C-G en ADN; en ARN la Timina se reemplaza por Uracilo.
const DNA_TO_RNA_COMPLEMENT = { A: 'U', T: 'A', C: 'G', G: 'C' };

// Tabla estándar del código genético (NCBI Genetic Code Table 1 / ExPASy).
// Codones de ARNm -> [nombre 3 letras, letra 1 código, categoría química]
const CODON_TABLE = {
  UUU:['Phe','F','nonpolar'], UUC:['Phe','F','nonpolar'],
  UUA:['Leu','L','nonpolar'], UUG:['Leu','L','nonpolar'],
  CUU:['Leu','L','nonpolar'], CUC:['Leu','L','nonpolar'], CUA:['Leu','L','nonpolar'], CUG:['Leu','L','nonpolar'],
  AUU:['Ile','I','nonpolar'], AUC:['Ile','I','nonpolar'], AUA:['Ile','I','nonpolar'],
  AUG:['Met','M','nonpolar'], // codón de inicio
  GUU:['Val','V','nonpolar'], GUC:['Val','V','nonpolar'], GUA:['Val','V','nonpolar'], GUG:['Val','V','nonpolar'],
  UCU:['Ser','S','polar'], UCC:['Ser','S','polar'], UCA:['Ser','S','polar'], UCG:['Ser','S','polar'],
  CCU:['Pro','P','nonpolar'], CCC:['Pro','P','nonpolar'], CCA:['Pro','P','nonpolar'], CCG:['Pro','P','nonpolar'],
  ACU:['Thr','T','polar'], ACC:['Thr','T','polar'], ACA:['Thr','T','polar'], ACG:['Thr','T','polar'],
  GCU:['Ala','A','nonpolar'], GCC:['Ala','A','nonpolar'], GCA:['Ala','A','nonpolar'], GCG:['Ala','A','nonpolar'],
  UAU:['Tyr','Y','polar'], UAC:['Tyr','Y','polar'],
  UAA:['STOP','*','stop'], UAG:['STOP','*','stop'],
  CAU:['His','H','basic'], CAC:['His','H','basic'],
  CAA:['Gln','Q','polar'], CAG:['Gln','Q','polar'],
  AAU:['Asn','N','polar'], AAC:['Asn','N','polar'],
  AAA:['Lys','K','basic'], AAG:['Lys','K','basic'],
  GAU:['Asp','D','acidic'], GAC:['Asp','D','acidic'],
  GAA:['Glu','E','acidic'], GAG:['Glu','E','acidic'],
  UGU:['Cys','C','polar'], UGC:['Cys','C','polar'],
  UGA:['STOP','*','stop'],
  UGG:['Trp','W','nonpolar'],
  CGU:['Arg','R','basic'], CGC:['Arg','R','basic'], CGA:['Arg','R','basic'], CGG:['Arg','R','basic'],
  AGU:['Ser','S','polar'], AGC:['Ser','S','polar'],
  AGA:['Arg','R','basic'], AGG:['Arg','R','basic'],
  GGU:['Gly','G','nonpolar'], GGC:['Gly','G','nonpolar'], GGA:['Gly','G','nonpolar'], GGG:['Gly','G','nonpolar'],
};

/* -------------------------------------------------------------------------
   2. NÚCLEO COMPUTACIONAL (funciones puras, sin dependencias del DOM)
   ------------------------------------------------------------------------- */

/** Valida que la secuencia solo contenga A, T, C, G (mayúsculas). */
function validarADN(seq) {
  return /^[ATCG]+$/.test(seq);
}

/** Transcribe una hebra molde de ADN a ARN mensajero (string). */
function transcribir(dna) {
  return dna.split('').map(b => DNA_TO_RNA_COMPLEMENT[b]).join('');
}

/** Encuentra el índice del primer codón de inicio AUG en el ARNm. */
function encontrarInicio(rna) {
  return rna.indexOf('AUG');
}

/** Divide el ARNm en codones (tripletes) a partir de un índice de inicio. */
function segmentarCodones(rna, inicio) {
  const codones = [];
  for (let i = inicio; i + 3 <= rna.length; i += 3) {
    codones.push(rna.slice(i, i + 3));
  }
  return codones;
}

/**
 * Traduce una lista de codones a proteína.
 * Devuelve { proteina: [{codon, nombre, letra, categoria}], detenidoPorParo, incompleto }
 */
function traducir(codones) {
  const proteina = [];
  let detenidoPorParo = false;
  for (const codon of codones) {
    const info = CODON_TABLE[codon];
    if (!info) { proteina.push({ codon, nombre:'???', letra:'?', categoria:'stop' }); continue; }
    const [nombre, letra, categoria] = info;
    proteina.push({ codon, nombre, letra, categoria });
    if (categoria === 'stop') { detenidoPorParo = true; break; }
  }
  return { proteina, detenidoPorParo, incompleto: !detenidoPorParo };
}

/* -------------------------------------------------------------------------
   3. CASOS DE VALIDACIÓN
   Estos casos se ejecutan en consola al cargar la página (F12 > Console)
   y comparan el resultado del simulador contra el resultado esperado según
   la tabla estándar del código genético (equivalente a ExPASy Translate).
   ------------------------------------------------------------------------- */
function ejecutarValidaciones() {
  const casos = [
    { dna: 'TACGGGAAATTCACT', esperado: 'Met-Pro-Phe-Lys-STOP' },
    { dna: 'TACCCGCTTCAGATT', esperado: 'Met-Gly-Glu-Val-STOP' },
    { dna: 'TACAAAACT',       esperado: 'Met-Phe-STOP' },
  ];
  let ok = 0;
  casos.forEach((c, idx) => {
    const rna = transcribir(c.dna);
    const inicio = encontrarInicio(rna);
    const codones = segmentarCodones(rna, inicio);
    const { proteina } = traducir(codones);
    const resultado = proteina.map(a => a.nombre).join('-');
    const pass = resultado === c.esperado;
    if (pass) ok++;
    console.log(`[Validación ${idx + 1}] ADN=${c.dna} -> ${resultado} | esperado=${c.esperado} | ${pass ? 'OK' : 'FALLÓ'}`);
  });
  console.log(`Validación completa: ${ok}/${casos.length} casos correctos.`);
}

/* -------------------------------------------------------------------------
   4. ESTADO Y ELEMENTOS DE INTERFAZ
   ------------------------------------------------------------------------- */
const state = {
  dna: '', rna: '', inicio: -1, codones: [], proteina: [],
  transcritoHasta: 0, codonActual: -1,
};

const el = id => document.getElementById(id);

function baseSpan(letra, dim) {
  return `<span class="base ${letra}${dim ? ' dim' : ''}">${letra}</span>`;
}

/* --- Barra de progreso --- */
function setProgress(paso) {
  el('progressFill').style.width = `${paso * 20}%`;
  document.querySelectorAll('.steps-labels span').forEach(s => {
    s.classList.toggle('current', Number(s.dataset.step) === paso);
  });
}

/* --- Pestañas --- */
document.querySelectorAll('nav.tabs button').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('nav.tabs button').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    ['sim', 'quiz', 'about'].forEach(t => { el('tab-' + t).style.display = 'none'; });
    el('tab-' + btn.dataset.tab).style.display = 'block';
  });
});

/* --- Ayuda guiada (toggle de paneles) --- */
function wireHelp(btnId, panelId) {
  el(btnId).addEventListener('click', () => el(panelId).classList.toggle('show'));
}
el('globalHelpBtn').addEventListener('click', () => el('globalHelp').classList.toggle('show'));
wireHelp('helpStep1', 'help1');
wireHelp('helpStep2', 'help2');
/* -------------------------------------------------------------------------
   5. PASO 1 -> 2: INICIO Y TRANSCRIPCIÓN
   ------------------------------------------------------------------------- */
el('exampleSelect').addEventListener('change', e => {
  if (e.target.value) el('dnaInput').value = e.target.value;
});

el('startBtn').addEventListener('click', () => {
  const raw = el('dnaInput').value.trim().toUpperCase();
  if (!raw) { el('inputError').textContent = 'Escribe una secuencia de ADN.'; return; }
  if (!validarADN(raw)) { el('inputError').textContent = 'La secuencia solo puede contener las letras A, T, C, G.'; return; }
  if (raw.length < 3) { el('inputError').textContent = 'La secuencia es demasiado corta (mínimo 3 bases).'; return; }
  el('inputError').textContent = '';

  state.dna = raw;
  state.rna = transcribir(raw);
  state.transcritoHasta = 0;

  renderStrands();
  el('step2').style.display = 'block';
  el('toStep3').disabled = true;
  setProgress(2);
  el('step2').scrollIntoView({ behavior: 'smooth' });
});

function renderStrands() {
  const dnaHtml = state.dna.split('').map(b => baseSpan(b, false)).join('');
  el('dnaStrand').innerHTML = dnaHtml;
  el('rnaStrand').innerHTML = '';
  el('linkRow').innerHTML = '';
}

let transcTimer = null;

function pintarBaseTranscrita(i) {
  const dnaBase = state.dna[i];
  const rnaBase = state.rna[i];
  // marca visualmente la base de ADN ya "leída"
  const dnaSpans = el('dnaStrand').children;
  dnaSpans[i].classList.add('pulse');

  const linkRow = el('linkRow');
  const mark = document.createElement('span');
  mark.className = 'link-mark';
  mark.textContent = '|';
  linkRow.appendChild(mark);

  const rnaSpan = document.createElement('span');
  rnaSpan.className = `base ${rnaBase} pulse`;
  rnaSpan.textContent = rnaBase;
  el('rnaStrand').appendChild(rnaSpan);

  state.transcritoHasta = i + 1;
  if (state.transcritoHasta >= state.dna.length) {
    el('toStep3').disabled = false;
  }
}

el('playTranscription').addEventListener('click', () => {
  clearInterval(transcTimer);
  transcTimer = setInterval(() => {
    if (state.transcritoHasta >= state.dna.length) { clearInterval(transcTimer); return; }
    pintarBaseTranscrita(state.transcritoHasta);
  }, 350);
});

el('skipTranscription').addEventListener('click', () => {
  clearInterval(transcTimer);
  while (state.transcritoHasta < state.dna.length) pintarBaseTranscrita(state.transcritoHasta);
});

el('toStep3').addEventListener('click', () => {
  prepararTraduccion();
  el('step34').style.display = 'block';
  setProgress(3);
  el('step34').scrollIntoView({ behavior: 'smooth' });
});

/* -------------------------------------------------------------------------
   6. PASO 3 -> 4: SEGMENTACIÓN EN CODONES Y TRADUCCIÓN
   ------------------------------------------------------------------------- */
function prepararTraduccion() {
  state.inicio = encontrarInicio(state.rna);
  if (state.inicio === -1) {
    el('codonTrack').innerHTML = '<span style="color:var(--bad)">No se encontró un codón de inicio (AUG) en este ARNm. Prueba otra secuencia.</span>';
    return;
  }
  state.codones = segmentarCodones(state.rna, state.inicio);
  state.codonActual = -1;
  state.proteina = [];
  renderCodonTrack();
  el('proteinChain').innerHTML = '';
  el('toStep5').disabled = true;
}

function renderCodonTrack() {
  const track = el('codonTrack');
  track.innerHTML = '';
  state.codones.forEach((codon, idx) => {
    const box = document.createElement('div');
    box.className = 'codon-box';
    box.id = `codon-${idx}`;
    if (idx === 0) box.classList.add('start');
    if (CODON_TABLE[codon] && CODON_TABLE[codon][2] === 'stop') box.classList.add('stop');
    codon.split('').forEach(b => {
      const s = document.createElement('div');
      s.className = `b base-${b}`;
      s.style.color = `var(--${b})`;
      s.textContent = b;
      box.appendChild(s);
    });
    track.appendChild(box);
  });
}

function moverRibosoma(idx) {
  let rib = el('ribosomeIcon');
  if (!rib) {
    rib = document.createElement('div');
    rib.id = 'ribosomeIcon';
    rib.className = 'ribosome';
    rib.textContent = '🧬';
    el('codonTrack').appendChild(rib);
  }
  const box = el(`codon-${idx}`);
  const trackRect = el('codonTrack').getBoundingClientRect();
  const boxRect = box.getBoundingClientRect();
  rib.style.left = `${boxRect.left - trackRect.left + boxRect.width / 2}px`;
  box.classList.add('active');
}

function traducirSiguienteCodon() {
  const idx = state.codonActual + 1;
  if (idx >= state.codones.length) return false;
  document.querySelectorAll('.codon-box.active').forEach(b => b.classList.remove('active'));
  const codon = state.codones[idx];
  const info = CODON_TABLE[codon] || ['???', '?', 'stop'];
  const [nombre, letra, categoria] = info;
  moverRibosoma(idx);
  state.codonActual = idx;
  state.proteina.push({ codon, nombre, letra, categoria });

  const bead = document.createElement('div');
  bead.className = `aa-bead ${categoria}`;
  bead.innerHTML = categoria === 'stop' ? 'STOP' : `<div>${letra}</div><div style="font-size:.5rem;">${nombre}</div>`;
  el('proteinChain').appendChild(bead);

  if (categoria === 'stop' || idx === state.codones.length - 1) {
    el('toStep5').disabled = false;
    return false;
  }
  return true;
}

el('stepCodon').addEventListener('click', () => { traducirSiguienteCodon(); });
el('skipCodon').addEventListener('click', () => { while (traducirSiguienteCodon()) {} });

el('toStep5').addEventListener('click', () => {
  renderResultado();
  el('step5').style.display = 'block';
  setProgress(5);
  el('step5').scrollIntoView({ behavior: 'smooth' });
});

/* -------------------------------------------------------------------------
   7. PASO 5: RESULTADO FINAL
   ------------------------------------------------------------------------- */
function renderResultado() {
  const chain = el('finalProtein');
  chain.innerHTML = '';
  state.proteina.forEach(aa => {
    const bead = document.createElement('div');
    bead.className = `aa-bead ${aa.categoria}`;
    bead.innerHTML = aa.categoria === 'stop' ? 'STOP' : `<div>${aa.letra}</div><div style="font-size:.5rem;">${aa.nombre}</div>`;
    chain.appendChild(bead);
  });

  const conParo = state.proteina.length && state.proteina[state.proteina.length - 1].categoria === 'stop';
  const numAA = state.proteina.filter(a => a.categoria !== 'stop').length;

  el('resultStats').innerHTML = `
    <div class="stat"><div class="n">${numAA}</div><div class="l">Aminoácidos</div></div>
    <div class="stat"><div class="n">${state.dna.length}</div><div class="l">Bases de ADN</div></div>
    <div class="stat"><div class="n">${conParo ? 'Sí' : 'No'}</div><div class="l">Codón de paro encontrado</div></div>
    <div class="stat"><div class="n">${state.inicio}</div><div class="l">Posición del AUG en el ARNm</div></div>
  `;
}

el('copyResult').addEventListener('click', () => {
  const texto = state.proteina.map(a => a.nombre).join('-');
  navigator.clipboard?.writeText(texto);
  el('copyResult').textContent = '¡Copiado!';
  setTimeout(() => { el('copyResult').textContent = 'Copiar secuencia de aminoácidos'; }, 1500);
});

el('restartBtn').addEventListener('click', () => location.reload());
el('goQuiz').addEventListener('click', () => document.querySelector('[data-tab="quiz"]').click());

/* -------------------------------------------------------------------------
   8. Autoevaluación de mutaciones
   ------------------------------------------------------------------------- */
const QUIZ_BASES = ['A', 'T', 'C', 'G'];

function generarPregunta() {
  // Secuencias base garantizadas con AUG y longitud múltiplo de 3.
  const bancos = ['TACCGGACGTTTATT', 'TACGTAGCACCTATT', 'TACTTTGGCAAAATT', 'TACACCCGTTCGATT'];
  const original = bancos[Math.floor(Math.random() * bancos.length)];
  const pos = 3 + Math.floor(Math.random() * (original.length - 4)); // evita mutar la 1ra base del AUG
  let nuevaBase;
  do { nuevaBase = QUIZ_BASES[Math.floor(Math.random() * 4)]; } while (nuevaBase === original[pos]);
  const mutada = original.slice(0, pos) + nuevaBase + original.slice(pos + 1);

  const proteinaOriginal = traducirCompleto(original);
  const proteinaMutada = traducirCompleto(mutada);

  let tipo;
  if (proteinaMutada.length !== proteinaOriginal.length) {
    tipo = 'nonsense'; // el codón de paro se movió: cambia la longitud
  } else {
    const igual = proteinaOriginal.every((a, i) => a.letra === proteinaMutada[i].letra);
    tipo = igual ? 'silenciosa' : 'missense';
  }

  return { original, mutada, pos, original_prot: proteinaOriginal, mutada_prot: proteinaMutada, tipo };
}

function traducirCompleto(dna) {
  const rna = transcribir(dna);
  const inicio = encontrarInicio(rna);
  const codones = segmentarCodones(rna, inicio);
  return traducir(codones).proteina;
}

function proteinaToStr(prot) { return prot.map(a => a.letra).join('-'); }

function renderQuiz() {
  const q = generarPregunta();
  const opciones = [
    { key: 'silenciosa', label: 'Mutación silenciosa (no cambia la proteína)' },
    { key: 'missense', label: 'Mutación missense (cambia un aminoácido)' },
    { key: 'nonsense', label: 'Mutación nonsense (crea/mueve un codón de paro)' },
  ];

  el('quizBody').innerHTML = `
    <div class="quiz-q">
      <div><b>ADN original:</b> ${q.original}</div>
      <div><b>ADN mutado:</b> &nbsp;${q.mutada.split('').map((b,i)=> i===q.pos ? `<span style="color:var(--accent);font-weight:700;">${b}</span>` : b).join('')}
        &nbsp; <span style="color:var(--muted);font-size:.75rem;">(posición ${q.pos + 1} cambió)</span></div>
    </div>
    <div class="quiz-options" id="quizOptions"></div>
    <div class="feedback" id="quizFeedback"></div>
  `;

  const optWrap = el('quizOptions');
  opciones.forEach(o => {
    const b = document.createElement('button');
    b.className = 'ghost';
    b.textContent = o.label;
    b.addEventListener('click', () => {
      document.querySelectorAll('#quizOptions button').forEach(x => x.disabled = true);
      const fb = el('quizFeedback');
      const correcto = o.key === q.tipo;
      fb.classList.add('show', correcto ? 'correct' : 'wrong');
      fb.innerHTML = `
        ${correcto ? '✅ ¡Correcto!' : '❌ No es correcto.'}
        La respuesta correcta es <b>${o.key === q.tipo ? o.label : opciones.find(x => x.key === q.tipo).label}</b>.<br>
        Proteína original: ${proteinaToStr(q.original_prot)}<br>
        Proteína mutada: &nbsp;${proteinaToStr(q.mutada_prot)}
      `;
    });
    optWrap.appendChild(b);
  });
}

el('newQuizBtn').addEventListener('click', renderQuiz);

/* -------------------------------------------------------------------------
   9. INICIALIZACIÓN
   ------------------------------------------------------------------------- */
window.addEventListener('DOMContentLoaded', () => {
  setProgress(1);
  ejecutarValidaciones();
  renderQuiz();
});

