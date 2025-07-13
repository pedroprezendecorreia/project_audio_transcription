# AI-Assisted Audio Recorder and Transcriber

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![PyQt6](https://img.shields.io/badge/PyQt6-6.x-green.svg)
![Whisper](https://img.shields.io/badge/Whisper-Model-lightgrey.svg)

## Overview

This project presents a Python application designed for local audio recording and transcription. It's a practical example of how modern AI tools can significantly accelerate development, allowing for rapid problem-solving and efficient creation of functional applications.

**Inspired by:** [WisprFlow.ai](https://wisprflow.ai/)

## Table of Contents

- [The Power of AI in Development](#the-power-of-ai-in-development)
- [Your Vision, Our Solution](#your-vision-our-solution)
- [Features](#features)
- [Technical Details](#technical-details)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the Application](#running-the-application)
- [Usage](#usage)
- [Known Issues & Future Improvements](#known-issues--future-improvements)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## The Power of AI in Development

This application was developed with the assistance of an AI agent (Manus). This collaboration demonstrates how AI can: 

- **Accelerate Development Cycles**: Solve real-world problems much faster than traditional methods.
- **Enhance Efficiency**: Achieve high levels of efficiency, comparable to human-only development.
- **Boost Scalability**: Provide a framework for highly scalable solutions.
- **Optimize Costs**: Deliver significant financial savings in development.

## Your Vision, Our Solution

While AI played a crucial role in the coding, the core of this project lies in human ingenuity and oversight. My contribution was essential in:

- **Problem Identification**: Pinpointing the real-world problem that this application solves.
- **Logical Structure Design**: Architecting the 'what', 'why', and 'how' of the solution.
- **Prompt Engineering**: Refining the instructions given to the AI to ensure optimal output.
- **Code Review and Testing**: Performing basic code revisions and rigorous testing to ensure functionality and quality.

This project is a testament to the synergy between human vision and AI capabilities, resulting in a robust and practical solution.

## Features

- **Local Audio Recording**: Record audio directly from your microphone.
- **Real-time Transcription**: Transcribe recorded audio using the powerful Whisper model.
- **Customizable Hotkeys**: Start and stop recording with a configurable keyboard shortcut.
- **Clipboard Integration**: Automatically copy transcribed text to your clipboard for easy pasting.
- **User-Friendly Interface**: Simple and intuitive graphical user interface (GUI) built with PyQt6.

## Technical Details

- **Programming Language**: Python
- **Key Libraries**:

| Library       | Purpose                               |
|---------------|---------------------------------------|
| `sounddevice` | Audio input/output                    |
| `soundfile`   | Audio file handling                   |
| `numpy`       | Numerical operations (audio data)     |
| `whisper`     | High-accuracy speech-to-text transcription |
| `PyQt6`       | Graphical User Interface (GUI)        |
| `keyboard`    | Global hotkey management              |
| `pyperclip`   | Clipboard operations                  |
| `configparser`| Managing application settings         |

## Getting Started

### Prerequisites

- Python 3.x
- `pip` (Python package installer)

### Installation

1. **Clone the repository (once available on GitHub)**:
   ```bash
   git clone [YOUR_GITHUB_REPO_URL]
   cd [YOUR_PROJECT_DIRECTORY]
   ```

2. **Install dependencies**:
   ```bash
   pip install sounddevice soundfile numpy whisper-cpp-python PyQt6 keyboard pyperclip
   ```
   *Note: For `whisper`, you might need to install `ffmpeg` separately depending on your operating system. Refer to the `whisper` library documentation for detailed instructions.*

### Running the Application

```bash
python main.py
```

## Usage

1. **Launch the application.**
2. **Configure your preferred hotkey** in the application interface.
3. **Select your desired Whisper model** (e.g., 'base', 'small', 'medium') for transcription accuracy vs. performance.
4. **Press the configured hotkey** to start recording. Press it again to stop.
5. **The transcribed text will automatically be copied to your clipboard.**

## Known Issues & Future Improvements

This project is actively under development. While functional, you might encounter:

- **Minor Bugs**: Some edge cases or unexpected behaviors may still exist.
- **UI/UX Enhancements**: The user interface is currently basic and will be improved in future iterations to offer a more polished and intuitive experience.

We are committed to continuous improvement and will address these areas in upcoming updates.


