# Shadowing App

Shadowing App is a work-in-progress application designed to assist users in learning foreign languages through the shadowing technique. The application enables users to play audio files, record their voices, and interact with timestamps for enhanced learning.

## Features
### Planned Core Features
- Audio playback (MP3, WAV, etc.).
- Play, pause, rewind, and fast-forward functionality.
- Interactive timeline with a draggable progress bar.
- Timestamp creation and management during audio playback.
- Storage of audio metadata and timestamps in a database.

### Additional Features
- Voice recording for shadowing exercises:
  - Users can listen to the audio, pause, and record their voice.
  - Playback includes both the recording and the original audio in sequence.
- Keyboard shortcuts for essential controls (e.g., spacebar for play/pause).
- Visual timeline markers for timestamps.

## Technologies
- **Python**: Core application logic.
- **Kivy**: User interface and screen management.
- **SQLite + SQLAlchemy**: Database for storing audio metadata and timestamps.
- **SoundLoader (Kivy)**: Audio playback.
- **PyInstaller**: Packaging the application into an executable file.

## Development Roadmap
1. **Set Up Environment**:
   - Define project structure.
   - Install necessary libraries (`kivy`, `sqlalchemy`, `pytest`).

2. **Basic Functionality**:
   - Implement file loading and playback.
   - Create a user-friendly interface for audio control.

3. **Database Integration**:
   - Design and implement models for audio metadata and timestamps.
   - Add functionality to save and retrieve user data.

4. **Advanced Features**:
   - Develop the recording feature for shadowing exercises.
   - Enhance the timeline with timestamp markers.

5. **Testing**:
   - Unit tests for audio and database logic.
   - Integration tests for seamless user interaction.

6. **Optimization and Packaging**:
   - Refine the UI and improve performance.
   - Package the application into an executable file.

## Current Status
This project is under active development. More details will be shared in upcoming commits and feature implementations.

---

Stay tuned for updates and feel free to contribute ideas or suggestions!
