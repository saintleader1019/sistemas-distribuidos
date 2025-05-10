<template>
  <q-page class="column items-center q-pa-md">
    <!-- Nombres superiores -->
    <div class="row justify-between items-center q-mb-md" style="width: 600px;">
      <div class="text-bold text-red">{{ jugadores[0].nombre }}</div>
      <div class="text-bold text-blue">{{ jugadores[1].nombre }}</div>
    </div>

    <!-- Tablero SVG basado en mapa lógico -->
    <div class="bg-grey-2" style="width: 600px; height: 600px; border: 2px solid #ccc;">
      <svg viewBox="0 0 15 15" width="100%" height="100%" shape-rendering="crispEdges">
        <template v-for="(row, fila) in boardMap" :key="`row-${fila}`">
          <template v-for="(cell, col) in row" :key="`cell-${fila}-${col}`">
            <rect
              :x="col" :y="fila" width="1" height="1"
              :fill="getCellColor(cell)"
              stroke="#888" stroke-width="0.03"
              @click="handleCellClick(fila, col)"
            />
          </template>
        </template>

        <!-- Centro (triángulo en cruz) -->
        <polygon points="7.5,7.5 6,6 9,6" fill="red" />
        <polygon points="7.5,7.5 6,9 6,6" fill="green" />
        <polygon points="7.5,7.5 9,9 6,9" fill="yellow" />
        <polygon points="7.5,7.5 9,6 9,9" fill="blue" />
      </svg>
    </div>

    <!-- Nombres inferiores -->
    <div class="row justify-between items-center q-mt-md" style="width: 600px;">
      <div class="text-bold text-green">{{ jugadores[2].nombre }}</div>
      <div class="text-bold text-yellow">{{ jugadores[3].nombre }}</div>
    </div>

    <!-- Zona de dados -->
    <div class="q-mt-md row q-gutter-md items-center justify-center">
      <div class="text-subtitle2">Dados:</div>
      <q-badge color="primary" class="text-h6">🎲 {{ dados[0] }}</q-badge>
      <q-badge color="primary" class="text-h6">🎲 {{ dados[1] }}</q-badge>
    </div>
  </q-page>
</template>

<script setup>
import { ref } from 'vue'

const jugadores = ref([
  { nombre: 'Jugador 1', color: 'red' },
  { nombre: 'Jugador 2', color: 'blue' },
  { nombre: 'Jugador 3', color: 'green' },
  { nombre: 'Jugador 4', color: 'yellow' },
])

const dados = ref([1, 6])

const boardMap = ref([
  ["home-red","home-red","home-red","home-red","home-red","home-red",null,       null,      null,       "home-blue","home-blue","home-blue","home-blue","home-blue","home-blue"],
  ["home-red",null,      null,      null,      null,      "home-red", null,       null,      null,       "home-blue",null,      null,      null,      null,      "home-blue"],
  ["home-red",null,      null,      null,      null,      "home-red", null,       null,      null,       "home-blue",null,      null,      null,      null,      "home-blue"],
  ["home-red",null,      null,      null,      null,      "home-red", null,       null,      null,       "home-blue",null,      null,      null,      null,      "home-blue"],
  ["home-red","home-red","home-red","home-red","home-red","home-red",null,       null,      null,       "home-blue","home-blue","home-blue","home-blue","home-blue","home-blue"],
  [null,     null,      null,      null,      null,      null,      null,       null,      null,       null,      null,      null,      null,      null,      null],
  [null,     null,      null,      null,      null,      null,      "path",   "path",   "path",    null,      null,      null,      null,      null,      null],
  [null,     null,      null,      null,      null,      null,      "path",   "center", "path",    null,      null,      null,      null,      null,      null],
  [null,     null,      null,      null,      null,      null,      "path",   "path",   "path",    null,      null,      null,      null,      null,      null],
  ["home-green","home-green","home-green","home-green","home-green","home-green",null,       null,      null,       "home-yellow","home-yellow","home-yellow","home-yellow","home-yellow","home-yellow"],
  ["home-green",null,      null,      null,      null,      "home-green", null,       null,      null,       "home-yellow",null,      null,      null,      null,      "home-yellow"],
  ["home-green",null,      null,      null,      null,      "home-green", null,       null,      null,       "home-yellow",null,      null,      null,      null,      "home-yellow"],
  ["home-green",null,      null,      null,      null,      "home-green", null,       null,      null,       "home-yellow",null,      null,      null,      null,      "home-yellow"],
  ["home-green",null,      null,      null,      null,      "home-green", null,       null,      null,       "home-yellow",null,      null,      null,      null,      "home-yellow"],
  ["home-green","home-green","home-green","home-green","home-green","home-green",null,       null,      null,       "home-yellow","home-yellow","home-yellow","home-yellow","home-yellow","home-yellow"]
])

function getCellColor(type) {
  return {
    "home-red": '#f44336',
    "home-blue": '#2196f3',
    "home-green": '#4caf50',
    "home-yellow": '#ffeb3b',
    "path": '#ffffff',
    "center": '#cccccc',
    null: '#ffffff'
  }[type] || '#ffffff'
}

function handleCellClick(fila, col) {
  console.log(`Casilla clic: fila ${fila}, columna ${col}`)
}
</script>

<style scoped>
.text-red { color: #f44336; }
.text-blue { color: #2196f3; }
.text-green { color: #4caf50; }
.text-yellow { color: #ffeb3b; }
</style>
