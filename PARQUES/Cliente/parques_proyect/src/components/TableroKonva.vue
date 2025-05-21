<template>
  <div class="q-pa-md flex flex-center">
    <div ref="containerRef" style="width: 600px; height: 600px;"></div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import Konva from 'konva'

const containerRef = ref(null)
const width = 600
const height = 600
const cellSize = 40
const grid = 15

onMounted(() => {
  const stage = new Konva.Stage({
    container: containerRef.value,
    width,
    height
  })

  const layer = new Konva.Layer()
  stage.add(layer)

  // Fondo del tablero (claro)
  const background = new Konva.Rect({
    x: 0,
    y: 0,
    width,
    height,
    fill: '#f8f8f8',
    stroke: '#ccc',
    strokeWidth: 2,
    cornerRadius: 10
  })
  layer.add(background)

  // Dibujar la grilla 15x15
  for (let row = 0; row < grid; row++) {
    for (let col = 0; col < grid; col++) {
      const cell = new Konva.Rect({
        x: col * cellSize,
        y: row * cellSize,
        width: cellSize,
        height: cellSize,
        stroke: '#ddd',
        strokeWidth: 0.5
      })
      layer.add(cell)
    }
  }

  // Agregar una ficha como círculo de prueba
  const ficha = new Konva.Circle({
    x: cellSize * 7.5,
    y: cellSize * 7.5,
    radius: 12,
    fill: 'red',
    stroke: 'black',
    strokeWidth: 1,
    draggable: true
  })
  layer.add(ficha)
  layer.draw()
})
</script>

<style scoped>
</style>
