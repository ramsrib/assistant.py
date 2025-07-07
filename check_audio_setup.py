#!/usr/bin/env python3
"""
Audio setup checker - shows current audio configuration and available devices
"""

import pyaudio
import subprocess
import os


def list_pyaudio_devices():
    """List PyAudio devices (what daily_call sees)"""
    print("🎵 PyAudio Devices (what daily_call.py sees):")
    print("=" * 60)

    audio = pyaudio.PyAudio()
    device_count = audio.get_device_count()

    for i in range(device_count):
        device_info = audio.get_device_info_by_index(i)
        print(f"Device {i}: {device_info['name']}")
        print(f"  Input Channels: {device_info['maxInputChannels']}")
        print(f"  Output Channels: {device_info['maxOutputChannels']}")
        print(f"  Sample Rate: {device_info['defaultSampleRate']}")
        print(
            f"  Host API: {audio.get_host_api_info_by_index(device_info['hostApi'])['name']}"
        )
        print("-" * 40)

    # Show default devices
    try:
        default_input = audio.get_default_input_device_info()
        default_output = audio.get_default_output_device_info()
        print(
            f"✅ Default Input: Device {default_input['index']} - {default_input['name']}"
        )
        print(
            f"✅ Default Output: Device {default_output['index']} - {default_output['name']}"
        )
        print(
            f"🔊 daily_call.py is currently using: Device {default_output['index']} for output"
        )
    except Exception as e:
        print(f"❌ Error getting default devices: {e}")

    audio.terminate()


def list_alsa_devices():
    """List ALSA devices (system level)"""
    print("\n🔧 ALSA Devices (system level):")
    print("=" * 60)

    try:
        # List ALSA cards
        result = subprocess.run(["aplay", "-l"], capture_output=True, text=True)
        if result.returncode == 0:
            print("ALSA Playback Devices:")
            print(result.stdout)
        else:
            print("❌ Could not list ALSA devices")
    except FileNotFoundError:
        print("❌ aplay command not found")

    try:
        # List ALSA capture devices
        result = subprocess.run(["arecord", "-l"], capture_output=True, text=True)
        if result.returncode == 0:
            print("ALSA Capture Devices:")
            print(result.stdout)
    except FileNotFoundError:
        print("❌ arecord command not found")


def check_current_daily_call_config():
    """Analyze daily_call.py configuration"""
    print("\n🔍 daily_call.py Configuration Analysis:")
    print("=" * 60)

    print("Current audio stream setup:")
    print("  - Sample Rate: 16000 Hz")
    print("  - Channels: 1 (mono)")
    print("  - Format: 16-bit PCM")
    print("  - Chunk Size: 640 frames")
    print("  - Output Device: DEFAULT (not specified)")
    print("  - Input Device: DEFAULT (not specified)")

    print("\n📝 Notes:")
    print("  - PyAudio is using the system default audio device")
    print("  - To use a specific device, you need to specify output_device_index")
    print("  - Your wm8960 sound card may not appear in PyAudio device list")


def suggest_modifications():
    """Suggest how to modify daily_call.py for specific devices"""
    print("\n💡 How to use specific audio device in daily_call.py:")
    print("=" * 60)

    print("To use a specific device, modify daily_call.py:")
    print()
    print("1. Find your desired device index from PyAudio list above")
    print("2. Modify the audio stream creation:")
    print()
    print("   # Original:")
    print("   self.__output_audio_stream = self.__audio_interface.open(")
    print("       format=pyaudio.paInt16,")
    print("       channels=NUM_CHANNELS,")
    print("       rate=SAMPLE_RATE,")
    print("       output=True,")
    print("       frames_per_buffer=CHUNK_SIZE,")
    print("   )")
    print()
    print("   # Modified (example for device 0):")
    print("   self.__output_audio_stream = self.__audio_interface.open(")
    print("       format=pyaudio.paInt16,")
    print("       channels=NUM_CHANNELS,")
    print("       rate=SAMPLE_RATE,")
    print("       output=True,")
    print("       output_device_index=0,  # <-- Add this line")
    print("       frames_per_buffer=CHUNK_SIZE,")
    print("   )")


def main():
    print("🎧 Audio Setup Diagnostic Tool")
    print("This tool helps identify which audio devices are available")
    print("and which device daily_call.py is currently using.\n")

    list_pyaudio_devices()
    list_alsa_devices()
    check_current_daily_call_config()
    suggest_modifications()


if __name__ == "__main__":
    main()
