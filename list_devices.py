import pyaudio


def list_audio_devices():
    """List all available audio devices"""
    audio = pyaudio.PyAudio()

    print("Available Audio Devices:")
    print("=" * 50)

    device_count = audio.get_device_count()

    for i in range(device_count):
        device_info = audio.get_device_info_by_index(i)

        print(f"Device {i}: {device_info['name']}")
        print(f"  Max Input Channels: {device_info['maxInputChannels']}")
        print(f"  Max Output Channels: {device_info['maxOutputChannels']}")
        print(f"  Default Sample Rate: {device_info['defaultSampleRate']}")
        print(
            f"  Host API: {audio.get_host_api_info_by_index(device_info['hostApi'])['name']}"
        )
        print("-" * 30)

    # Show default devices
    default_input = audio.get_default_input_device_info()
    default_output = audio.get_default_output_device_info()

    print(f"Default Input Device: {default_input['index']} - {default_input['name']}")
    print(
        f"Default Output Device: {default_output['index']} - {default_output['name']}"
    )

    audio.terminate()


if __name__ == "__main__":
    list_audio_devices()
