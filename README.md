# Pokémon Battle Simulator

## Laboratory Hands-on #3

### Objective(s)

The goal is to develop a Pokémon battle simulator using key data structures like arrays, linked lists, stacks, queues, and trees. This project will apply these structures to create a functional battle system.

- **List**: Stores the Pokémon's attributes, including its name, health, power, and type.
- **Linked List**: Used for both Player 1 and Player 2 to store their selected Pokémon teams.
- **Queue**: Manages the battle sequences, ensuring that actions are carried out in the correct order.
- **Stack**: Manages temporary effects such as potions and poison. These effects will be added to the stack when applied and removed once their duration expires.
- **Tree**: Monitors and records the outcomes of each battle, keeping detailed results and determining the overall winner based on the highest number of match wins.

### Program

This program is the final version of the Pokémon game, developed as part of a group project. The team enhanced the user experience by creating an improved graphical user interface (GUI) using Pygame. This update aims to make the game more enjoyable, interactive, and visually appealing for players.

Along with the updated GUI, the program uses various data structures such as arrays, linked lists, stacks, queues, and trees. These structures are employed to manage key game elements like Pokémon teams, moves, battle mechanics, and events. The program is designed to meet all required goals and objectives, ensuring a smooth and engaging gaming experience. This final version highlights the team's focus on improving both the technical features and overall user experience.

### Algorithm

1. **START**
2. The program will prompt Player One (1) to select their Pokémon first, followed by Player Two (2). This process will continue until both players have assembled a team of three Pokémon each.
3. The program will then randomly choose a battlefield for the Pokémon to engage in their battle.
4. Before each battle, players will have the option to choose whether to use poison, potion, or run, but this choice will only be available under certain conditions. The first battle will be between the first Pokémon chosen by each player. After that match, the program randomly selects a new battlefield, and the second Pokémon from each player will battle. This process will continue until all three Pokémon from each team have fought. The game will proceed until one team's Pokémon are all defeated or a player chooses to run.
5. Finally, the overall winner will be announced once all battles are completed and one team has defeated the other or if a player chooses to run.
6. **END**

### Libraries and Dependencies

To run this project, you will need to install the following libraries:

- `pygame`: Used for creating the graphical user interface (GUI).
- `pillow`: Used for image manipulation and processing.
- `random`: Standard Python library for generating random numbers.
- `os`: Standard Python library for interacting with the operating system.
- `threading`: Standard Python library for running multiple threads concurrently.

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/ZyrusAlvez/pokemon-battle-simulator.git
