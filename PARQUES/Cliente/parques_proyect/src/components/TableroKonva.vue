<template>
  <div class="q-pa-md flex flex-center">
    <v-stage :config="stageConfig">
      <v-layer>
        <!-- Fondo del tablero -->
        <v-rect :config="{
          x: 0,
          y: 0,
          width: width,
          height: height,
          fill: '#f5f5f5',
          stroke: '#bbb',
          strokeWidth: 4,
          cornerRadius: 16
        }" />

        <!-- Cuadrícula optimizada -->
        <template v-for="i in grid * grid" :key="i">
          <v-rect :config="{
            x: ((i - 1) % grid) * cellSize,
            y: Math.floor((i - 1) / grid) * cellSize,
            width: cellSize,
            height: cellSize,
            stroke: '#ddd',
            strokeWidth: 0.5
          }" />
        </template>
      </v-layer>
    </v-stage>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { Stage as VStage, Layer as VLayer, Rect as VRect } from '@konva/vue3'

const width = 600
const height = 600
const cellSize = 40
const grid = 15

const stageConfig = ref({
  width,
  height,
  draggable: false
})
</script>

<style scoped>
</style>
