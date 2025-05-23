import Phaser from 'phaser'
import GameScene from './scenes/GameScene.js'

const config = {
  type: Phaser.AUTO,
  width: 600,
  height: 600,
  backgroundColor: '#f8f8f8',
  scene: [GameScene],
}

new Phaser.Game(config)
