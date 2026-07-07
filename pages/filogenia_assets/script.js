/* =========================================================================
   SIMULADOR DE FILOGENIA — ALGORITMO UPGMA
   -------------------------------------------------------------------------
   1. Núcleo computacional (función pura ejecutarUPGMA)
   2. Casos de validación (consola)
   3. Lógica de interfaz, envuelta en DOMContentLoaded para evitar el error
      "Cannot read properties of null" si el script se ejecuta antes de
      que el HTML termine de cargar.
   ========================================================================= */

/* -------------------------------------------------------------------------
   1. NÚCLEO COMPUTACIONAL (no depende del DOM)
   ------------------------------------------------------------------------- */

/**
 * Ejecuta el algoritmo UPGMA completo sobre una matriz de distancias.
 * @param {number[][]} matrizInicial - matriz NxN de distancias.
 * @param {string[]} especiesIniciales - nombres de las N especies (mismo orden que la matriz).
 * @returns {{pasos: Array, arbolFinal: string}} - lista de fusiones realizadas y el HTML del árbol final.
 */
function ejecutarUPGMA(matrizInicial, especiesIniciales) {
  // Clusters iniciales: cada especie es su propio grupo
  let clusters = especiesIniciales.map(function (nombre) {
    return { etiqueta: nombre, tamaño: 1, html: `<div class="hoja">${nombre}</div>` };
  });

  // Copiamos la matriz para no dañar la original
  let matriz = matrizInicial.map(function (fila) { return fila.slice(); });

  let pasos = [];

  // Se repite hasta que quede un solo grupo (la raíz del árbol)
  while (clusters.length > 1) {
    let menor = Infinity, filaMin = 0, colMin = 1;

    for (let i = 0; i < clusters.length; i++) {
      for (let j = i + 1; j < clusters.length; j++) {
        if (matriz[i][j] < menor) { menor = matriz[i][j]; filaMin = i; colMin = j; }
      }
    }

    const clusterA = clusters[filaMin];
    const clusterB = clusters[colMin];
    const nuevoTamaño = clusterA.tamaño + clusterB.tamaño;

    const nuevoCluster = {
      etiqueta: `(${clusterA.etiqueta}-${clusterB.etiqueta})`,
      tamaño: nuevoTamaño,
      html: `
        <div class="nodo">
          <div class="grupo">(${clusterA.etiqueta}-${clusterB.etiqueta})</div>
          <div class="lineaVertical"></div>
          <div class="lineaHorizontal"></div>
          <div class="hijos">${clusterA.html}${clusterB.html}</div>
        </div>
      `,
    };

    pasos.push({ especieA: clusterA.etiqueta, especieB: clusterB.etiqueta, distancia: menor });

    // Recalcular distancias del nuevo clúster hacia los demás (promedio ponderado)
    const nuevosClusters = [];
    const indicesRestantes = [];
    for (let k = 0; k < clusters.length; k++) {
      if (k !== filaMin && k !== colMin) { nuevosClusters.push(clusters[k]); indicesRestantes.push(k); }
    }

    const nuevaMatriz = [];
    for (let i = 0; i < indicesRestantes.length; i++) {
      const filaNueva = [];
      for (let j = 0; j < indicesRestantes.length; j++) {
        filaNueva.push(matriz[indicesRestantes[i]][indicesRestantes[j]]);
      }
      const distA = matriz[filaMin][indicesRestantes[i]];
      const distB = matriz[colMin][indicesRestantes[i]];
      filaNueva.push((clusterA.tamaño * distA + clusterB.tamaño * distB) / nuevoTamaño);
      nuevaMatriz.push(filaNueva);
    }

    const ultimaFila = indicesRestantes.map(function (idx) {
      const distA = matriz[filaMin][idx];
      const distB = matriz[colMin][idx];
      return (clusterA.tamaño * distA + clusterB.tamaño * distB) / nuevoTamaño;
    });
    ultimaFila.push(0);
    nuevaMatriz.push(ultimaFila);

    nuevosClusters.push(nuevoCluster);
    clusters = nuevosClusters;
    matriz = nuevaMatriz;
  }

  return { pasos: pasos, arbolFinal: clusters[0].html };
}

/* -------------------------------------------------------------------------
   2. VALIDACIÓN (se ejecuta en consola al cargar la página, F12 > Console)
   Caso de referencia calculado y verificado manualmente:
   Matriz Perro/Lobo/Zorro/Coyote -> fusiones: (Perro-Lobo)=2, (Zorro-Coyote)=5,
   ((Perro-Lobo)-(Zorro-Coyote))=7.5
   ------------------------------------------------------------------------- */
function ejecutarValidaciones() {
  const matriz = [[0, 2, 8, 7], [2, 0, 9, 6], [8, 9, 0, 5], [7, 6, 5, 0]];
  const especies = ['Perro', 'Lobo', 'Zorro', 'Coyote'];
  const esperado = [
    { especieA: 'Perro', especieB: 'Lobo', distancia: 2 },
    { especieA: 'Zorro', especieB: 'Coyote', distancia: 5 },
    { especieA: '(Perro-Lobo)', especieB: '(Zorro-Coyote)', distancia: 7.5 },
  ];
  const resultado = ejecutarUPGMA(matriz, especies).pasos;
  let ok = true;
  resultado.forEach((paso, i) => {
    const e = esperado[i];
    const pass = paso.especieA === e.especieA && paso.especieB === e.especieB && paso.distancia === e.distancia;
    if (!pass) ok = false;
    console.log(`[Validación UPGMA ${i + 1}] obtenido=(${paso.especieA}, ${paso.especieB}, d=${paso.distancia}) | esperado=(${e.especieA}, ${e.especieB}, d=${e.distancia}) | ${pass ? 'OK' : 'FALLÓ'}`);
  });
  console.log(`Validación completa: ${ok ? 'todos los casos correctos' : 'hay fallos, revisar ejecutarUPGMA'}.`);
}

/* -------------------------------------------------------------------------
   3. INTERFAZ (envuelto en DOMContentLoaded)
   ------------------------------------------------------------------------- */
document.addEventListener('DOMContentLoaded', function () {

  ejecutarValidaciones();

  const el = id => document.getElementById(id);

  const btnReiniciar = el('btnReiniciar');
  const btnEjemplo = el('btnEjemplo');
  const btnConstruir = el('btnConstruir');
  const ayuda1 = el('ayuda1');
  const ayuda2 = el('ayuda2');
  const ayuda3 = el('ayuda3');
  const barra = el('barra');
  const explicacion = el('explicacion');
  const arbolDiv = el('arbol');
  const estadoAlgoritmo = el('estadoAlgoritmo');
  const errorMatriz = el('errorMatriz');

  const IDS_MATRIZ = ['a1', 'a2', 'a3', 'a4', 'b1', 'b2', 'b3', 'b4', 'c1', 'c2', 'c3', 'c4', 'd1', 'd2', 'd3', 'd4'];
  const MAPA_CELDAS = { '0-1': 'celda_a2', '0-2': 'celda_a3', '0-3': 'celda_a4', '1-2': 'celda_b3', '1-3': 'celda_b4', '2-3': 'celda_c4' };

  estadoAlgoritmo.innerHTML = '🔴 Esperando datos...';

  /* ----- Cargar ejemplo ----- */
  btnEjemplo.addEventListener('click', function (event) {
    event.preventDefault(); // Evita recargas imprevistas dentro del iframe de Streamlit
    el('espA').value = 'Perro'; el('espB').value = 'Lobo'; el('espC').value = 'Zorro'; el('espD').value = 'Coyote';
    el('a1').value = 0; el('a2').value = 2; el('a3').value = 8; el('a4').value = 7;
    el('b1').value = 2; el('b2').value = 0; el('b3').value = 9; el('b4').value = 6;
    el('c1').value = 8; el('c2').value = 9; el('c3').value = 0; el('c4').value = 5;
    el('d1').value = 7; el('d2').value = 6; el('d3').value = 5; el('d4').value = 0;

    errorMatriz.textContent = '';
    explicacion.innerHTML = '✅ Se cargó correctamente una matriz de ejemplo. Ahora presiona "Construir árbol".';
    estadoAlgoritmo.innerHTML = '🟢 Matriz de ejemplo cargada.';
  });

  /* ----- Utilidades ----- */
  function avanzarBarra(valorFinal) {
    let progreso = Number(barra.value);
    const intervalo = setInterval(function () {
      progreso++;
      barra.value = progreso;
      if (progreso >= valorFinal) clearInterval(intervalo);
    }, 15);
  }

  function obtenerMatriz() {
    return [
      [Number(el('a1').value), Number(el('a2').value), Number(el('a3').value), Number(el('a4').value)],
      [Number(el('b1').value), Number(el('b2').value), Number(el('b3').value), Number(el('b4').value)],
      [Number(el('c1').value), Number(el('c2').value), Number(el('c3').value), Number(el('c4').value)],
      [Number(el('d1').value), Number(el('d2').value), Number(el('d3').value), Number(el('d4').value)],
    ];
  }

  /** Valida que la matriz tenga solo números válidos y no negativos. */
  function validarMatriz() {
    for (const id of IDS_MATRIZ) {
      const valor = el(id).value.trim();
      if (valor === '' || isNaN(Number(valor)) || Number(valor) < 0) {
        return `El campo "${id}" debe ser un número mayor o igual a 0.`;
      }
    }
    return null;
  }

  function limpiarResaltado() {
    document.querySelectorAll('.resaltada').forEach(c => c.classList.remove('resaltada'));
  }

  function resaltarPrimeraCelda(matriz) {
    let menor = Infinity, fila = 0, columna = 0;
    for (let i = 0; i < 4; i++) {
      for (let j = i + 1; j < 4; j++) {
        if (matriz[i][j] < menor) { menor = matriz[i][j]; fila = i; columna = j; }
      }
    }
    const id = MAPA_CELDAS[`${fila}-${columna}`];
    if (id && el(id)) el(id).classList.add('resaltada');
  }

  /* ----- Construir árbol (algoritmo completo) ----- */
  btnConstruir.addEventListener('click', function (event) {
    event.preventDefault(); // Protege la ejecución de eventos extraños en la nube
    const errorMsg = validarMatriz();
    if (errorMsg) { errorMatriz.textContent = '⚠️ ' + errorMsg; return; }
    errorMatriz.textContent = '';

    const especies = [el('espA').value || 'Especie A', el('espB').value || 'Especie B', el('espC').value || 'Especie C', el('espD').value || 'Especie D'];
    const matriz = obtenerMatriz();

    limpiarResaltado();
    resaltarPrimeraCelda(matriz);

    const upgma = ejecutarUPGMA(matriz, especies);

    barra.value = 0;
    arbolDiv.innerHTML = '';
    explicacion.innerHTML = '🔍 Iniciando el algoritmo UPGMA...';
    estadoAlgoritmo.innerHTML = '🟡 Analizando la matriz de distancias...';
    avanzarBarra(10);

    const numPasos = upgma.pasos.length;
    upgma.pasos.forEach(function (paso, index) {
      setTimeout(function () {
        explicacion.innerHTML += `<br><br>🌳 Paso ${index + 1}: se agrupó <strong>${paso.especieA}</strong> con <strong>${paso.especieB}</strong> (distancia = ${paso.distancia.toFixed(2)}).`;
        avanzarBarra(10 + Math.round((index + 1) * (80 / numPasos)));
      }, 1100 * (index + 1));
    });

    const tiempoFinal = 1100 * (numPasos + 1);
    setTimeout(function () {
      arbolDiv.innerHTML = upgma.arbolFinal;
      estadoAlgoritmo.innerHTML = '🟢 Árbol filogenético completo construido.';
      avanzarBarra(100);
    }, tiempoFinal);
  });

  /* ----- Reiniciar ----- */
  btnReiniciar.addEventListener('click', function (event) {
    event.preventDefault(); // Asegura estabilidad al resetear el componente
    barra.value = 0;
    explicacion.innerHTML = 'El simulador ha sido reiniciado.';
    arbolDiv.innerHTML = 'Todavía no se ha generado.';
    estadoAlgoritmo.innerHTML = '🔴 Esperando datos...';
    errorMatriz.textContent = '';
    limpiarResaltado();

    IDS_MATRIZ.forEach(id => { el(id).value = 0; });
    el('espA').value = 'Especie A'; el('espB').value = 'Especie B'; el('espC').value = 'Especie C'; el('espD').value = 'Especie D';

    document.querySelectorAll('.opcion').forEach(function (opcion) {
      opcion.classList.remove('correcta', 'incorrecta');
      opcion.style.pointerEvents = 'auto';
    });
    ['respuesta1', 'respuesta2', 'respuesta3'].forEach(id => { el(id).innerHTML = ''; });
  });

  /* ----- Ayuda guiada ----- */
  ayuda1.addEventListener('click', function (event) {
    event.preventDefault();
    el('textoAyuda').innerHTML = `
      <strong>¿Qué es UPGMA?</strong><br><br>
      UPGMA significa <em>Unweighted Pair Group Method using Arithmetic Averages</em>.
      Es un algoritmo utilizado para construir árboles filogenéticos agrupando primero
      las especies (o clústeres) que presentan la menor distancia genética.
    `;
  });

  ayuda2.addEventListener('click', function (event) {
    event.preventDefault();
    el('textoAyuda').innerHTML = `
      <strong>¿Cómo calcula las distancias?</strong><br><br>
      Cuando UPGMA une dos especies o grupos, calcula la distancia del nuevo grupo hacia
      los demás usando el <strong>promedio ponderado</strong> de las distancias originales,
      considerando cuántos miembros tiene cada grupo.
    `;
  });

  ayuda3.addEventListener('click', function (event) {
    event.preventDefault();
    el('textoAyuda').innerHTML = `
      <strong>¿Para qué sirve un árbol filogenético?</strong><br><br>
      Un árbol filogenético representa las relaciones evolutivas entre organismos y
      muestra cuáles especies comparten un ancestro común más reciente.
    `;
  });

  /* ----- Quiz / autoevaluación (CORREGIDO PARA EVITAR RECARGAS) ----- */
  function activarPregunta(clase, respuestaId) {
    const opciones = document.querySelectorAll('.' + clase);
    opciones.forEach(function (opcion) {
      opcion.addEventListener('click', function (event) {
        event.preventDefault(); // 👈 FIJADO: Evita el colapso del Quiz en servidores cloud
        opciones.forEach(o => { o.style.pointerEvents = 'none'; });
        const respuesta = el(respuestaId);
        if (opcion.hasAttribute('data-correcta')) {
          opcion.classList.add('correcta');
          respuesta.innerHTML = '✅ ¡Respuesta correcta!';
        } else {
          opcion.classList.add('incorrecta');
          respuesta.innerHTML = '❌ Respuesta incorrecta.';
          opciones.forEach(o => { if (o.hasAttribute('data-correcta')) o.classList.add('correcta'); });
        }
      });
    });
  }

  activarPregunta('pregunta1', 'respuesta1');
  activarPregunta('pregunta2', 'respuesta2');
  activarPregunta('pregunta3', 'respuesta3');

});