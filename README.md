# HandLight Dash - Gesture-Based Python Game

![Screenshot (180)](https://github.com/maskboyAvi/HandLight-Dash/assets/123640350/b824ecd8-e645-49c9-b97a-2a9a28a36118)

HandLight Dash is an interactive Python-based game inspired by the classic "Red Light, Green Light." In this game, players must perform specific hand gestures to earn points when the light is green, while staying still during the red light phase. The game features a custom-trained Convolutional Neural Network (CNN) model that interprets players' gestures. Players need to achieve 100 points to win, earning 10 points for each correct gesture during the green light phase. However, if they move during the red light phase, the game ends.

## Gameplay Rules

- **Objective:** Earn 100 points by making correct gestures during the green light phase.
- **Gestures:** The game recognizes five gestures: "HI," "ROCK," "PEACE," "ThumbsUP," and "OK."
- **Green Light:** Perform the correct gesture to earn 10 points during the green light phase.
- **Red Light:** Stay still and do not perform any gestures during the red light phase.
- **Winning:** Accumulate 100 points to win the game.
- **Losing:** Moving during the red light phase ends the game.
- **Restart:** Press 'R' to restart the game at any time.

## Installation

1. Install the required Python libraries using the following command:

   ```bash
   pip install opencv-python cvzone numpy tensorflow tk Pillow screeninfo
   ```

2. Run the `main.py` script to start the game:

   ```bash
   python main.py
   ```

## Model Evaluation

The game utilizes a custom-trained CNN model to recognize hand gestures. The model has been trained on five gestures: "HI," "ROCK," "PEACE," "ThumbsUP," and "OK." The model evaluation process includes the following steps:

1. **Image Capture:** The game captures the player's hand gesture using the webcam.
2. **Gesture Recognition:** The captured image is processed using the CNN model to identify the gesture.
3. **Green Light:** During the green light phase, players need to make the correct gesture to earn points.
4. **Red Light:** The game will transition to a red light phase, during which players should not move.
5. **Score Calculation:** The game calculates and displays the player's score based on correct gestures.

![Screenshot (179)](https://github.com/maskboyAvi/HandLight-Dash/assets/123640350/63a945d8-3670-463e-b44d-c93a9515c7a6)

## Game Play

![Screenshot (182)](https://github.com/maskboyAvi/HandLight-Dash/assets/123640350/6d7718e0-c30b-4301-98a8-d1aa8bc88ab4)
![Screenshot (181)](https://github.com/maskboyAvi/HandLight-Dash/assets/123640350/917fdcbb-3c5d-40e8-97d1-392be340d84f)
![Winner](https://github.com/maskboyAvi/HandLight-Dash/assets/123640350/82beef26-b838-4dce-b1f6-fbb87c91cbd8)
![Screenshot (183)](https://github.com/maskboyAvi/HandLight-Dash/assets/123640350/ab0e6f3b-53c6-4832-811d-17aebae28d3e)

## Contributing
Contributions are welcome! If you find any issues or have suggestions, please create an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
