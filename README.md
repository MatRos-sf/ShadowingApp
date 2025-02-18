# Shadowing App

Shadowing App is a completed application designed to assist users in learning foreign languages through the shadowing technique or practicing dictation. The application enables users to play audio files, manage timestamps, and offers a variety of interactive features. Recording functionality is planned for future updates.

## Features

### Core Features
- Audio playback (MP3, WAV, etc.)
- Play, pause, rewind, and fast-forward functionality
- Interactive timeline with a draggable progress bar
- Timestamp creation and management during audio playback
- Storage of audio metadata and timestamps in a database

### Additional Features
- Voice recording for shadowing exercises (planned for a future update)
- Keyboard shortcuts for essential controls (e.g., spacebar for play/pause):
    - Arrow Keys:
        - **Left Arrow**: Rewind audio
        - **Right Arrow**: Fast forward audio
        - **Up Arrow**: Play audio
        - **Down Arrow**: Add timestamp
    - **Spacebar**: Pause audio
    - **R**: Remove timestamp
- Visual timeline markers for timestamps

## Technologies
- **Python3.12**: Core application logic
- **Kivy**: User interface and screen management
- **SQLAlchemy**: Database for storing audio metadata and timestamps
- **SoundLoader (Kivy)**: Audio playback

## Installation

1. **Set Up Environment**:
   ```sh
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
2. **Run app**
```sh
python3 main.py
```

## Notes
- The application has been tested only on Linux systems.
- This application is ideal for individuals looking to practice shadowing or dictation techniques to improve their language skills.
- Recording functionality: A voice recording feature is planned and will be added in a future update.
- **Automated Tests:** Tests are automatically executed during pull requests on GitHub to ensure code quality.
## Project Structure
Here is a brief overview of the project structure:

```
shadowing_app/
├── audio/          # User's audio files
├── recordings/     # User's recordings
├── database/       # Database (SQLite)
│   ├── models.py   # SQLAlchemy data models
│   └── db_setup.py # Database setup and configuration
├── ui/             # Kivy interface-related files
│   ├── screens.py  # Application screen definitions
│   └── kv/         # KV files for layouts
├── utils/          # Utility functions (e.g., for audio handling)
│   ├── audio.py    # Audio playback and rewinding logic
│   └── timestamps.py # Timestamp management
├── main.py         # Application entry point
└── tests/          # Application tests
```

## Screenshots

Here are some screenshots of the application in action:
![Zrzut ekranu z 2025-02-18 21-22-26](https://github.com/user-attachments/assets/ac04fd93-9425-4a44-8677-f157e031901e)
![Zrzut ekranu z 2025-02-18 21-22-46](https://github.com/user-attachments/assets/55b3c829-74bf-4da3-b263-f26549947a3c)
![Zrzut ekranu z 2025-02-18 21-22-59](https://github.com/user-attachments/assets/611daac0-d71b-49d9-b709-374af71aceec)
![Zrzut ekranu z 2025-02-18 21-23-05](https://github.com/user-attachments/assets/33e76c99-76ca-4d29-9e31-e2e53647ac32)
![Zrzut ekranu z 2025-02-18 21-23-16](https://github.com/user-attachments/assets/e6b92563-9873-4709-9b2a-adfe78736ec2)
![Zrzut ekranu z 2025-02-18 21-23-33](https://github.com/user-attachments/assets/628f37aa-af23-4cd3-808d-17c00e6f4381)

