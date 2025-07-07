# assistant.py 🔬

Voice assistant on Raspberry Pi

## Features

- **Audio Processing**: pyaudio
- **Voice AI**: vapi.ai

## Prerequisites

- Docker installed on your system
- Make (optional, for using Makefile commands)

## Quick Start

1. **Build the Docker image**

   ```bash
   make build
   # or without make:
   # docker build -t assistant.py .
   ```

2. **Run the application**

   ```bash
   make run
   # or without make:
   # docker run --rm assistant.py
   ```

## Makefile Commands

| Command | Description |
|---------|-------------|
| `make build` | Build the Docker image |
| `make run` | Run the container (executes main.py) |
| `make run-env` | Run with environment variables from .env file |
| `make shell` | Open an interactive bash shell in the container |
| `make dev` | Run with volume mount for development (live code reload) |
| `make python` | Open a Python REPL in the container |
| `make logs` | Show container logs |
| `make stop` | Stop the running container |
| `make clean` | Remove container and image |

## Environment Variables

Create a `.env` file in the project root (copy from `.env.example`):

```bash
API_KEY=your_api_key_here
VAPI_API_KEY=your_vapi_api_key_here
DAILY_API_KEY=your_daily_api_key_here
```

## Development

### Running in Development Mode

Use the development mode to mount your local code into the container:

```bash
make dev
```

This allows you to edit code locally and run it immediately in the container without rebuilding.

### Project Structure

```
assistant.py/
├── Dockerfile          # Docker configuration
├── Makefile           # Build and run commands
├── requirements.txt   # Python dependencies
├── main.py           # Main application script
├── .env              # Environment variables (create from .env.example)
└── README.md         # This file
```

### Adding New Dependencies

1. Add the package to `requirements.txt`
2. Rebuild the Docker image: `make build`

### Creating New Scripts

1. Create your Python script in the project directory
2. Run it using:

   ```bash
   docker run --rm -v $(PWD):/app assistant.py python3 your_script.py
   ```

## Audio Examples

### Basic Audio Recording (sounddevice)

```python
import sounddevice as sd
import numpy as np

# Record 5 seconds of audio
duration = 5  # seconds
fs = 44100    # Sample rate
recording = sd.rec(int(duration * fs), samplerate=fs, channels=2)
sd.wait()     # Wait until recording is finished
```

### Audio Playback (pyaudio)

```python
import pyaudio
import numpy as np

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=44100,
                output=True)
# Generate and play a tone
t = np.linspace(0, 1, 44100)
tone = np.sin(2 * np.pi * 440 * t)  # 440 Hz
stream.write(tone.astype(np.float32).tobytes())
stream.close()
p.terminate()
```

## Troubleshooting

### Audio Device Issues

If you encounter audio device issues on Raspberry Pi:

1. Ensure audio devices are properly connected
2. Check device permissions
3. You might need to run Docker with additional privileges:

   ```bash
   docker run --rm --privileged assistant.py
   ```

### Environment Variables Not Loading

- Ensure `.env` file exists in the project root
- Use `make run-env` instead of `make run`
- Check file permissions on `.env`

## Contributing

Feel free to submit issues and enhancement requests!

## License

[Your License Here]
