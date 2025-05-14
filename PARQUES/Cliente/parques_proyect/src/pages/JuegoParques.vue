<template>
  <q-page class="column items-center q-pa-md">
    <!-- Nombres superiores -->
    <div class="row justify-between items-center q-mb-md" style="width: 600px;">
      <div class="text-bold text-red">Jugador 1</div>
      <div class="text-bold text-blue">Jugador 2</div>
    </div>

    <!-- Tablero Konva -->
    <TableroKonva />

    <!-- Nombres inferiores -->
    <div class="row justify-between items-center q-mt-md" style="width: 600px;">
      <div class="text-bold text-green">Jugador 3</div>
      <div class="text-bold text-yellow">Jugador 4</div>
    </div>

    <!-- Zona de dados -->
    <div class="q-mt-md row q-gutter-md items-center justify-center">
      <div class="text-subtitle2">Dados:</div>
      <q-badge color="primary" class="text-h6">🎲 1</q-badge>
      <q-badge color="primary" class="text-h6">🎲 6</q-badge>
    </div>
  </q-page>
</template>

<script setup>
import TableroKonva from 'components/TableroKonva.vue'
</script>

<style scoped>
.text-red { color: #f44336; }
.text-blue { color: #2196f3; }
.text-green { color: #4caf50; }
.text-yellow { color: #ffeb3b; }
</style>
