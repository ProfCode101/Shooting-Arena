# 3D Bullet Frenzy

A 3D shooting arena game built with Python and OpenGL. Fight off waves of enemies in a colorful 3D arena while managing your health and accuracy.

## Features

- **3D Graphics**: Immersive 3D environment with OpenGL rendering
- **Multiple Camera Views**: Switch between first-person and third-person perspectives
- **Enemy AI**: Enemies spawn and actively chase the player
- **Health System**: Start with 5 health points - avoid enemy collisions!
- **Score Tracking**: Earn points by eliminating enemies
- **Auto-Play Mode**: Watch the game play itself with automatic aiming and shooting
- **Dynamic Arena**: Checkerboard-patterned floor with colorful boundary walls

## Requirements

### Dependencies

- Python 3.x
- PyOpenGL
- PyOpenGL-accelerate (optional, for better performance)

### Installation

Install the required packages using pip:

```bash
pip install PyOpenGL PyOpenGL-accelerate
```

On some systems, you may also need to install GLUT:

**Windows:**
- GLUT is typically included with PyOpenGL

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install freeglut3-dev
```

**macOS:**
```bash
brew install freeglut
```

## How to Run

Simply execute the Python script:

```bash
python shooting_game.py
```

## Gameplay

### Objective

Survive as long as possible by eliminating enemies before they reach you. The game ends when:
- Your health reaches 0 (enemies collide with you)
- You miss 10 shots

### Controls

#### Movement
- **W** - Move forward
- **S** - Move backward
- **A** - Turn left (only when auto-play is disabled)
- **D** - Turn right (only when auto-play is disabled)

#### Combat
- **Left Mouse Click** - Shoot a bullet in the direction you're facing

#### Camera
- **Right Mouse Click** - Toggle between first-person and third-person view
- **Arrow Keys** - Adjust camera position in third-person view (UP/DOWN/LEFT/RIGHT)

#### Special Modes
- **C** - Toggle auto-play/cheat mode (automatically aims and shoots at enemies)
- **V** - Toggle gun view in auto-play mode (shows gun perspective)

#### Game Management
- **R** - Restart the game (when game over)

### Game Mechanics

- **Health**: You start with 5 health points. Each enemy collision reduces health by 1.
- **Score**: Earn 1 point for each enemy eliminated.
- **Missed Shots**: Bullets that leave the arena count as misses. Game ends after 10 missed shots.
- **Enemy Spawning**: Up to 5 enemies spawn at a time. When one is eliminated, a new one spawns.
- **Enemy Behavior**: Enemies move toward your position and have a pulsating animation.

### Auto-Play Mode

Press **C** to enable auto-play mode, which:
- Automatically rotates the agent
- Detects enemies in the line of fire
- Automatically shoots when an enemy is aligned
- Increases movement speed
- Provides larger hit detection radius
- Allows bullets to hit enemies even when leaving the arena

## Game States

### Running
- Health, score, and missed shots are displayed
- Gameplay is active

### Game Over
- Final score is displayed
- Press **R** to restart

## Technical Details

- **Window Size**: 1000x600 pixels
- **Arena Size**: 14x14 tile grid (1400x1400 units)
- **Field of View**: 120 degrees
- **Bullet Speed**: 10 units per frame
- **Opponent Speed**: 0.05 units per frame
- **Max Opponents**: 5
- **Max Missed Bullets**: 10

## Tips

1. Keep moving to avoid enemy collisions
2. Aim carefully - missed shots count against you
3. Use third-person view to get better situational awareness
4. Try auto-play mode to see optimal aiming strategies
5. Manage your health - each collision is costly!

## License

This project is open source and available for educational purposes.

## Author

Created as a 3D graphics and game development project. 

## Email : tasnimdrmc6461@gmail.com

