import { casillas } from './casillas.js'

export default class GameScene extends Phaser.Scene {
  constructor() {
    super('GameScene')
  }

  preload() {
    this.load.image('tablero', '/tablero.png')
  }

  create() {
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
    this.turnoText = this.add.text(20, 20, '', {
      fontSize: '18px',
      fontStyle: 'bold',
      color: '#000'
    })

    this.socket = new WebSocket('ws://localhost:8000/ws')

    this.socket.onopen = () => {
      console.log('✅ Conectado al backend')
    }

    this.socket.onmessage = (event) => {
      const data = JSON.parse(event.data)
      console.log('📥 Estado recibido del backend:', data)

      if (data.accion === 'rechazado') {
        if (this.alertaTexto) this.alertaTexto.destroy()
        this.alertaTexto = this.add.text(20, 70, `🚫 ${data.motivo}`, {
          fontSize: '16px',
          color: '#ff0000',
          backgroundColor: '#ffffff',
          padding: { left: 10, right: 10, top: 5, bottom: 5 }
        }).setScrollFactor(0).setDepth(100).setAlpha(0.95)

        this.time.delayedCall(3000, () => {
          if (this.alertaTexto) this.alertaTexto.destroy()
        })
        return
      }

      if (data.accion === 'mover' && data.jugador && data.nuevaCasillaId !== undefined) {
        const ficha = this.fichas.find(f => f.getData('jugador') === data.jugador && f.getData('fichaId') === data.fichaId)
        const destino = casillas.find(c => c.id === data.nuevaCasillaId)
        if (ficha && destino) {
          ficha.setPosition(destino.x, destino.y)
          ficha.setData('casillaId', destino.id)
        }
      }

      if (data.turno) {
        this.turnoActual = data.turno
        this.turnoText.setText(`Turno: ${this.turnoActual}`)
      }
    }

    this.socket.onerror = (err) => {
      console.error('❌ Error en WebSocket:', err)
    }

    this.fichas = []

    colores.forEach(color => {
      const carceles = casillas.filter(c => c.tipo === 'carcel' && c.color === color)
      carceles.forEach((casilla, index) => {
        const fichaContainer = this.add.container(casilla.x, casilla.y)
        const circulo = this.add.circle(0, 0, 15, colorMap[color])
        circulo.setStrokeStyle(2, 0x000000)
        const inicial = this.add.text(-6, -8, color.charAt(0).toUpperCase(), {
          fontSize: '16px',
          fontStyle: 'bold',
          color: '#000'
        })
        fichaContainer.add([circulo, inicial])
        fichaContainer.setData('jugador', color)
        fichaContainer.setData('fichaId', index)
        fichaContainer.setData('casillaId', casilla.id)

        fichaContainer.setSize(30, 30)
        fichaContainer.setInteractive({ useHandCursor: true })
        fichaContainer.on('pointerdown', () => {
          const jugador = fichaContainer.getData('jugador')
          const fichaId = fichaContainer.getData('fichaId')

          if (jugador !== this.turnoActual) {
            console.log(`🚫 No es el turno de ${jugador}`)
            return
          }

          console.log(`🎯 Ficha ${fichaId} de ${jugador} clickeada`)

          this.socket.send(JSON.stringify({
            accion: 'mover',
            jugador,
            fichaId
          }))
        })

        this.fichas.push(fichaContainer)
      })
    })
  }
}
