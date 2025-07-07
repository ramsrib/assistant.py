import pyaudio
import wave
import time


def find_wm8960_devices():
    """Find WM8960 input and output device indices"""
    audio = pyaudio.PyAudio()

    input_device = None
    output_device = None

    for i in range(audio.get_device_count()):
        device_info = audio.get_device_info_by_index(i)
        name = device_info["name"].lower()

        if "wm8960" in name or "soundcard" in name:
            if device_info["maxInputChannels"] > 0:
                input_device = i
                print(f"Found WM8960 input device: {i} - {device_info['name']}")
            if device_info["maxOutputChannels"] > 0:
                output_device = i
                print(f"Found WM8960 output device: {i} - {device_info['name']}")

    audio.terminate()
    return input_device, output_device


def record_with_pyaudio(device_index, duration=5, filename="recording.wav"):
    """Record audio using specific device"""

    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2  # WM8960 expects stereo
    RATE = 44100

    audio = pyaudio.PyAudio()

    try:
        # Open stream with specific input device
        stream = audio.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            input_device_index=device_index,
            frames_per_buffer=CHUNK,
        )

        print(f"Recording from device {device_index} for {duration} seconds...")

        frames = []
        for i in range(0, int(RATE / CHUNK * duration)):
            data = stream.read(CHUNK)
            frames.append(data)

        print("Recording finished")

        # Stop and close stream
        stream.stop_stream()
        stream.close()

        # Save as WAV file
        wf = wave.open(filename, "wb")
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b"".join(frames))
        wf.close()

        print(f"Saved recording as {filename}")
        return filename

    except Exception as e:
        print(f"Recording error: {e}")
        return None
    finally:
        audio.terminate()


def play_with_pyaudio(device_index, filename):
    """Play audio using specific device"""

    try:
        # Open WAV file
        wf = wave.open(filename, "rb")

        audio = pyaudio.PyAudio()

        # Open stream with specific output device
        stream = audio.open(
            format=audio.get_format_from_width(wf.getsampwidth()),
            channels=wf.getnchannels(),
            rate=wf.getframerate(),
            output=True,
            output_device_index=device_index,
        )

        print(f"Playing on device {device_index}...")

        # Read and play data
        CHUNK = 1024
        data = wf.readframes(CHUNK)

        while data:
            stream.write(data)
            data = wf.readframes(CHUNK)

        # Clean up
        stream.stop_stream()
        stream.close()
        wf.close()
        audio.terminate()

        print("Playback finished")

    except Exception as e:
        print(f"Playback error: {e}")


def record_and_play_test():
    """Test recording and playback with WM8960"""

    # Find WM8960 devices
    input_dev, output_dev = find_wm8960_devices()

    if input_dev is None:
        print("WM8960 input device not found!")
        return

    if output_dev is None:
        print("WM8960 output device not found!")
        return

    # Record audio
    filename = record_with_pyaudio(input_dev, duration=5)

    if filename:
        # Play it back
        time.sleep(1)  # Brief pause
        play_with_pyaudio(output_dev, filename)


if __name__ == "__main__":
    print("Testing PyAudio with specific devices...")
    record_and_play_test()
