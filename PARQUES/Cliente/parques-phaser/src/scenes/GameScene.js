// Código actualizado con soporte para nombre de jugador, botón de inicio y sincronización con backend
import { casillas } from './casillas.js'

export default class GameScene extends Phaser.Scene {
  constructor() {
    super('GameScene')
    this.moveMarkers = []
    this.fichaSeleccionada = null
    this.dado1 = 0
    this.dado2 = 0
  }

  preload() {
    console.log('[Phaser] Preload assets')
    this.load.image('tablero', '/tablero.png')
    for (let i = 1; i <= 6; i++) {
      this.load.image(`dado${i}`, `/dados/dado${i}.png`)
    }
  }

  create() {
    const nombreJugador = prompt("Ingresa tu nombre para unirte a la partida:") || 'Jugador'
    this.nombreJugador = nombreJugador

    const scale = 1
    const tablero = this.add.image(this.cameras.main.centerX, this.cameras.main.centerY, 'tablero')
    tablero.setOrigin(0.5, 0.5)
    tablero.setScale(scale)
    this.cameras.main.setBackgroundColor('#f0f0f0')

    const colores = ['rojo', 'amarillo', 'azul', 'verde']
    const colorMap = {
      rojo: 0xff4d4d,
      amarillo: 0xffe066,
      azul: 0x4d94ff,
      verde: 0x4dff88
    }

    this.turnoActual = null
    this.nombreTurno = ''
    this.estadoTurno = 'esperando_lanzamiento'
    this.valoresDisponibles = []
    this.valorSeleccionado = null
    this.miColor = null

    this.turnoText = this.add.text(20, 20, '', {
      fontSize: '18px', fontStyle: 'bold', color: '#000'
    })

    this.dadoSprite1 = this.add.image(420, 800, 'dado1').setScale(0.2)
    this.dadoSprite2 = this.add.image(480, 800, 'dado1').setScale(0.2)

    this.botonesDados = []

    this.lanzarBtn = this.add.text(380, 850, '🎲 Lanzar', {
      fontSize: '22px', backgroundColor: '#4caf50', color: '#fff', padding: { x: 10, y: 5 }
    }).setInteractive({ useHandCursor: true })

    this.lanzarBtn.on('pointerdown', () => {
      console.log('[UI] Botón lanzar presionado')
      if (this.estadoTurno !== 'esperando_lanzamiento') return
      this.lanzarBtn.disableInteractive()
      const jugador = this.miColor
      this.socket.send(JSON.stringify({ accion: 'lanzar_dados', jugador }))
    })

    this.socket = new WebSocket('ws://localhost:8000/ws')

    this.socket.onopen = () => {
      this.socket.send(JSON.stringify({ accion: 'registro', nombre: nombreJugador }))
    }

    this.fichas = []
    this.socket.onmessage = (event) => {
      const data = JSON.parse(event.data)
      console.log('[RECEPCIÓN]', data)

      if (data.accion === 'esperando_inicio') {
        this.miColor = data.color
      }

      if (data.accion === 'mostrar_boton_inicio') {
        const btnInicio = this.add.text(300, 400, 'Iniciar Partida', {
          fontSize: '24px', backgroundColor: '#1976d2', color: '#fff', padding: { x: 20, y: 10 }
        }).setInteractive({ useHandCursor: true })

        btnInicio.on('pointerdown', () => {
          this.socket.send(JSON.stringify({ accion: 'iniciar_partida' }))
          btnInicio.destroy()
        })
      }

      if (data.accion === 'estado_inicial') {
        this.turnoActual = data.turno
        this.nombreTurno = data.nombre_turno
        this.turnoText.setText(`Turno de: ${this.nombreTurno}`)
        this.spawnFichas(colores, colorMap)
      }

      if (data.accion === 'resultado_dados') {
        const { dado1, dado2, valores } = data
        this.dado1 = dado1
        this.dado2 = dado2
        this.dadoSprite1.setTexture(`dado${dado1}`)
        this.dadoSprite2.setTexture(`dado${dado2}`)
        this.estadoTurno = 'esperando_movimiento'
        this.valoresDisponibles = valores
        console.log(`[UI] Valores disponibles actualizados: ${valores.join(', ')}`)
        this.renderBotonesValores()
        console.log(`[UI] Botones renderizados para: ${this.valoresDisponibles.join(', ')}`)
      }

      if (data.accion === 'rechazado') {
        if (data.reintentar) {
          this.estadoTurno = 'esperando_lanzamiento'
          this.lanzarBtn.setInteractive({ useHandCursor: true })
        }
      }

      if (data.accion === 'mover') {
        const ficha = this.fichas.find(f => f.getData('jugador') === data.jugador && f.getData('fichaId') === data.fichaId)
        const destino = casillas.find(c => c.id === data.nuevaCasillaId)
        if (ficha && destino) {
          ficha.setPosition(destino.x, destino.y)
          ficha.setData('casillaId', destino.id)
        }

        this.valoresDisponibles = data.restantes || []
        console.log(`[UI] Valores disponibles actualizados: ${this.valoresDisponibles.join(', ')}`)
        this.clearMoveMarkers()
        this.renderBotonesValores()

        if (this.valoresDisponibles.length === 0) {
          this.estadoTurno = 'esperando_lanzamiento'
          this.turnoActual = data.turno
          this.nombreTurno = data.nombre_turno
          this.turnoText.setText(`Turno de: ${this.nombreTurno}`)
          this.lanzarBtn.setInteractive({ useHandCursor: true })
        }
      }

      if (data.accion === 'pasar_turno') {
        this.turnoActual = data.turno
        this.nombreTurno = data.nombre_turno
        this.estadoTurno = 'esperando_lanzamiento'
        this.turnoText.setText(`Turno de: ${this.nombreTurno}`)
        this.lanzarBtn.setInteractive({ useHandCursor: true })
      }
    }
  }

  spawnFichas(colores, colorMap) {
    colores.forEach(color => {
      const carceles = casillas.filter(c => c.tipo === 'carcel' && c.color === color)
      carceles.forEach((casilla, index) => {
        const fichaContainer = this.add.container(casilla.x, casilla.y)
        const circulo = this.add.circle(0, 0, 15, colorMap[color])
        circulo.setStrokeStyle(2, 0x000000)
        const inicial = this.add.text(-6, -8, color.charAt(0).toUpperCase(), {
          fontSize: '16px', fontStyle: 'bold', color: '#000'
        })
        fichaContainer.add([circulo, inicial])
        fichaContainer.setData('jugador', color)
        fichaContainer.setData('fichaId', index)
        fichaContainer.setData('casillaId', casilla.id)

        circulo.setInteractive({ useHandCursor: true })
        circulo.on('pointerdown', () => {
          if (color !== this.miColor || this.estadoTurno !== 'esperando_movimiento') return

          const fichaId = fichaContainer.getData('fichaId')
          const casillaId = fichaContainer.getData('casillaId')
          const estaEnCarcel = casillas.find(c => c.id === casillaId)?.tipo === 'carcel'
          if (estaEnCarcel) {
            const suma = this.dado1 + this.dado2
            if (!isNaN(suma)) {
              this.socket.send(JSON.stringify({
                accion: 'mover', jugador: color, fichaId, valor: suma
              }))
            }
            return
          }

          this.fichaSeleccionada = fichaContainer
          this.drawMoveMarkers(fichaId, casillaId)
        })

        this.fichas.push(fichaContainer)
      })
    })
  }

  drawMoveMarkers(fichaId, casillaActual) {
    this.clearMoveMarkers()
    this.valoresDisponibles.forEach(valor => {
      const destinoId = (casillaActual + valor) % 68
      const destino = casillas.find(c => c.id === destinoId)
      if (destino) {
        const marker = this.add.rectangle(destino.x, destino.y, 12, 12, 0x000000).setInteractive()
        marker.setData('fichaId', fichaId)
        marker.setData('valor', valor)
        marker.on('pointerdown', () => {
          const jugador = this.miColor
          const valor = marker.getData('valor')

          if (!this.valoresDisponibles.includes(valor)) return

          this.socket.send(JSON.stringify({ accion: 'mover', jugador, fichaId, valor }))
          this.clearMoveMarkers()

          const btnUsado = this.botonesDados.find(b => b.getData('valor') === valor)
          if (btnUsado) {
            btnUsado.setStyle({ backgroundColor: '#999' })
            btnUsado.disableInteractive()
          }

          if (this.valoresDisponibles.length === 0) {
            this.estadoTurno = 'esperando_lanzamiento'
            this.lanzarBtn.setInteractive({ useHandCursor: true })
          } else {
            this.renderBotonesValores()
          }
        })
        this.moveMarkers.push(marker)
      }
    })
  }

  clearMoveMarkers() {
    this.moveMarkers.forEach(marker => marker.destroy())
    this.moveMarkers = []
  }

  renderBotonesValores() {
    this.botonesDados.forEach(b => b.destroy())
    this.botonesDados = []
    const startX = 250
    const startY = 920
    const spacing = 80
    this.valoresDisponibles.forEach((valor, index) => {
      const btn = this.add.text(startX + index * spacing, startY, `${valor}`, {
        fontSize: '20px', backgroundColor: '#2196f3', color: '#fff', padding: { x: 10, y: 5 }
      }).setInteractive({ useHandCursor: true })
      btn.on('pointerdown', () => {
        this.valorSeleccionado = valor
        this.botonesDados.forEach(b => b.setStyle({ backgroundColor: '#2196f3' }))
        btn.setStyle({ backgroundColor: '#1565c0' })
      })
      btn.setData('valor', valor)
      this.botonesDados.push(btn)
    })
  }
}
