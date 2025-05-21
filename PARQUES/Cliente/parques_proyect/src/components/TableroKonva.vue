<template>
  <div class="q-pa-md flex flex-center">
    <div ref="containerRef" style="width: 600px; height: 600px;"></div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import Konva from 'konva'
import { useImage } from '@vueuse/core'


const containerRef = ref(null)
const width = 600
const height = 600

onMounted(async () => {
  const stage = new Konva.Stage({
    container: containerRef.value,
    width,
    height,
  })

  const layer = new Konva.Layer()
  stage.add(layer)

  // Fondo claro con borde
  const background = new Konva.Rect({
    x: 0,
    y: 0,
    width,
    height,
    fill: '#f5f5f5',
    stroke: '#ccc',
    strokeWidth: 4,
    cornerRadius: 16,
  })
  layer.add(background)

  // Cargar imagen del tablero (opcional)
  const { image } = useImage(new URL('C:/Users/santi/OneDrive/Documentos/GitHub/sistemas-distribuidos/PARQUES/Cliente/parques_proyect/src/assets/Tablero.png', import.meta.url).href)
  const checkImageReady = () => {
    if (image.value) {
      const fondo = new Konva.Image({
        x: 0,
        y: 0,
        width,
        height,
        image: image.value,
      })
      layer.add(fondo)
      layer.draw()
    } else {
      setTimeout(checkImageReady, 100)
    }
  }
  checkImageReady()
})
</script>

<style scoped>
</style>
