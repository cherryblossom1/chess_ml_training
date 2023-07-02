# Chess Music Generator

This project aims to generate music based on chess games. By combining the moves played in a chess game with musical elements, we can create unique and harmonious compositions. The goal is to develop a machine learning-based approach to generate musical patterns that correlate with the chess moves.

## Roadmap

1. Data Collection:
   - Explore the Lichess API or available datasets to gather a large collection of chess games. This will serve as the training data for the ML model.
   - Design a function or script that can efficiently retrieve game data from Lichess and store it locally.
   - We use 'https://database.lichess.org/' for database

2. PGN Parsing:
   - Extend the existing PGN parsing capabilities to handle the large dataset collected. Ensure the parsing process is optimized for efficiency to handle a high volume of games.

3. Feature Engineering:
   - Determine the relevant features for training the ML model. These could include move types, piece positions, game outcomes, and any additional features that may influence the musical composition.
   - Design a mapping mechanism that assigns musical attributes (such as frequencies or notes) to the extracted features. This mapping will be used during training and music generation.

4. Model Training:
   - Select an appropriate ML algorithm for the task, such as a neural network or decision tree-based model.
   - Split the dataset into training and testing sets to evaluate the model's performance.
   - Train the model using the training set and fine-tune hyperparameters to optimize its performance.
   - Validate the model using the testing set and measure its accuracy and generalization capabilities.

5. Music Generation:
   - Once the model is trained, use it to generate music for new chess moves.
   - Given a chess move as input, pass it through the model to predict the corresponding musical attributes.
   - Use the mapping mechanism to convert the predicted attributes into actual musical notes or patterns.

6. Training and Testing Iterations:
   - Continuously iterate on the model training process, adjusting hyperparameters, and incorporating user feedback to improve the quality of music generation.
   - Explore different ML architectures and techniques to enhance the model's performance.
   - Regularly test the model on new chess games and evaluate its ability to generate pleasing and coherent musical compositions.

## Getting Started

To start this project, follow these steps:

1. Set up the project environment and install the required dependencies.
2. Begin with Step 1 of the roadmap: Data Collection.
3. Proceed through each step, implementing the necessary components and refining the model as you progress.

## First Attempt
1. Taken a Lichess dataset of some 4L games played by random individuals from 'https://database.lichess.org/'

2. The [training](read_game.py) script parses through this dataset and assigns frequencies to individual unique moves from a bounded frequency range. 
   - This assignment is chosen as per 'dissonance' cost function which is a rough estimate of how melodius consecutive frequencies will sound. There are other measures, but for simplicity we go with this.
   - The unique move-set along with assigned frequencies is stored in [datafile](unique_moves.txt).
   - No neural-network based approaches for training. We used brute-force.

3. Once the "training" is completed, testing can be performed using [test](test_game.py). Separate [test directory](pgn_files) is provided to check how each game "sounds".

## License

This project is licensed under the [Apache License 2.0](LICENSE.md).

Apache License
Version 2.0, January 2004
http://www.apache.org/licenses/

Copyright July 2023 Parth Mehta and ChatGPT

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
