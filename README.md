This Python project is an Aim Trainer Game built using the Pygame library. It is designed to help players improve their reflexes and aiming precision by clicking on growing and shrinking targets that appear on the screen. The game becomes progressively more difficult by reducing the time between target spawns as the player successfully hits more targets.

Key Features:
Dynamic Targets: Targets appear at random positions on the screen. They grow in size until reaching a maximum, then shrink until they disappear. Players must click on them before they vanish to score points.

Level Progression: The difficulty increases as players score hits, with targets spawning more frequently after every 10 hits. The spawn interval reduces by 10% to keep the game challenging.

Lives System: Players have 10 lives, which are reduced when they miss targets. The game ends when all lives are lost, displaying the final statistics like total time, speed (targets hit per second), total hits, and accuracy.

Score Display: A top bar shows the current game stats, including elapsed time, hits, lives remaining, and the current level.

End Screen: After the player loses all lives, an end screen shows their performance, including time played, hit speed, accuracy, and the number of targets hit. Players can restart the game from this screen.

User Interface: The game uses a combination of labels and buttons to provide feedback and control options, creating an engaging user experience.

This project demonstrates proficiency in Pygame for creating interactive games, including handling user input, real-time updates, target animations, and game mechanics such as scorekeeping and increasing difficulty levels.
