# Lecture Sound Refiner

**Lecture Sound Refiner** is a Python-based tool designed to enhance the audio quality of lecture recordings. It uses AI to separate speech from other audio elements, then applies compression, EQ and limiting to produce a clean and balanced final MP3 file.

## Features
- **AI Speech Separation**: Uses Demucs to isolate speech from background noise and music.
- **Audio Enhancement**: Applies equalization (EQ) to balance frequencies, compression for dynamic range control, and limiting to ensure consistent volume levels.
- **MP3 Output**: Final processed audio is saved as a high-quality MP3 file.

## Requirements
This project requires Python 3.x and several dependencies for audio processing, AI model inference, and file handling. Please follow the steps below to set up your environment.

### Dependencies:
- **Demucs**: AI model for separating speech from background audio.
- **Pedalboard**: Audio processing library to apply EQ, compression, and limiting.
- **Soundfile**: Library for reading and writing audio files.
- **Pyloudnorm**: For loudness normalization
- **Torch**: Core machine learning library for running the Demucs model.

## Installation

1. **Clone the repository**:

```bash
git clone https://github.com/AdamRopelewski/LectureSoundRefiner.git
cd LectureSoundRefiner
```

2. **Set up a virtual environment** (recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use venv\Scripts\activate
```

3. **Install dependencies** using the provided `requirements.txt` file:

```bash
pip install -r requirements.txt
```

This will install the necessary libraries for audio separation and processing. Note that `requirements.txt` includes a special PyTorch installation with CUDA 12.4 support for GPU acceleration.


## Usage

TODO

The `main.py` script will:
- Use Demucs to separate speech from background elements.
- Apply EQ, compression, and limiting.
- Save the final processed audio as `output.mp3`.

### Example Command:

```bash

```

### Script Explanation
- **Demucs for Speech Separation**: The AI model Demucs is used to isolate the speech from the background noise and music. This allows the tool to focus on refining just the speech portion for clarity and intelligibility.
   
- **EQ (Equalization)**: Frequencies are adjusted to ensure a balanced and clear voice. Low frequencies (such as rumble) are reduced, while the mid-range frequencies (where speech resides) are enhanced.
   
- **Compression**: The dynamic range of the speech is compressed to make quiet parts louder and louder parts quieter, resulting in a more consistent volume throughout the lecture.

- **Limiting**: The final step is limiting, which prevents clipping by ensuring the audio doesn't exceed the desired volume levels.

