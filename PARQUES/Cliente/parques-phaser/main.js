import Phaser from 'phaser'
import GameScene from './src/scenes/GameScene.js'

const config = {
  type: Phaser.AUTO,
  width: 900,
  height: 900,
  backgroundColor: '#000000',
  scene: [GameScene]
}

new Phaser.Game(config)