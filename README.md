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
- Keyboard shortcuts for essential controls (e.g., spacebar for play/pause)
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
