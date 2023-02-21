# Hex-AI-Bot

This is a Python project that implements an AI bot to play the famous Hex game. The bot is designed to use a combination of Dijkstra's algorithm and minimax search with alpha-beta pruning to select its moves, with the help of transposition tables to reduce complexity.

While the bot does not have a 100% win rate against a randomised bot, it follows a mixed strategy to find the most profitable hex to play at each turn, in order to try and find a path to victory. This makes the bot a challenging opponent for anyone looking to play Hex.

## Installation
To use the Hex AI Bot, you will need to have Python 3.x installed on your computer, along with the following packages:

NumPy </br>
Pygame</br>
You can install these packages using pip, the Python package manager. Once you have installed Python and the required packages, you can download the project repository from Github and run the "hex.py" file to start playing against the bot.

## Usage
To start a game against the Hex AI Bot, simply run the "hex.py" file using Python, and follow the instructions provided by the interface. You can choose to play as either the "X" or "O" player, and the bot will make its moves using its Dijkstra-minimax algorithm.

During the game, the interface will display the current state of the board, along with any messages or prompts that are relevant to the current turn. You can use the mouse to select the hex you want to play on, and the bot will respond with its own move.

## Contributing
If you are interested in contributing to the Hex AI Bot project, feel free to fork the repository and submit a pull request with your changes. We welcome contributions of all kinds, including bug fixes, feature additions, and documentation improvements.

Please make sure to follow our code of conduct and contributing guidelines, which can be found in the repository's "CONTRIBUTING.md" file.

## License
The Hex AI Bot project is licensed under the MIT License, which means that you are free to use, modify, and distribute the code as you see fit, as long as you include the original license and copyright notice.

## Acknowledgements
This project was inspired by the Hex game, as well as by the many AI algorithms and techniques that have been developed for playing games like chess, Go, and poker. We would like to thank the open source community for providing so many useful tools and libraries that make it possible to build projects like this one.
