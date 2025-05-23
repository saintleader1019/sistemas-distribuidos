export default class GameScene extends Phaser.Scene {
  constructor() {
    super('GameScene')
  }

  preload() {
    // Aquí puedes cargar assets en el futuro
  }

  create() {
    this.add.text(200, 280, '¡Tablero Parqués!', {
      fontSize: '24px',
      color: '#000',
    })
  }
}
