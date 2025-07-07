#!/usr/bin/env python3
"""
Audio System Diagnostic Tool
Checks which audio system is running and provides correct commands
"""

import subprocess
import os


def check_pulseaudio():
    """Check if PulseAudio is running"""
    try:
        result = subprocess.run(
            ["pulseaudio", "--check", "-v"], capture_output=True, text=True
        )
        if result.returncode == 0:
            print("✅ PulseAudio is running")
            return True
        else:
            print("❌ PulseAudio is not running")
            return False
    except FileNotFoundError:
        print("❌ PulseAudio not installed")
        return False


def list_pulse_sinks():
    """List PulseAudio sinks if available"""
    try:
        result = subprocess.run(
            ["pactl", "list", "short", "sinks"], capture_output=True, text=True
        )
        if result.returncode == 0:
            print("\n🔊 PulseAudio Sinks (Output Devices):")
            print("-" * 50)
            for line in result.stdout.strip().split("\n"):
                if line:
                    parts = line.split("\t")
                    if len(parts) >= 2:
                        sink_id = parts[0]
                        sink_name = parts[1]
                        print(f"  {sink_id}: {sink_name}")
                        if "wm8960" in sink_name.lower() or "hw_2" in sink_name:
                            print(f"    ⭐ This is your WM8960 device!")
            return True
        else:
            print("❌ Could not list PulseAudio sinks")
            return False
    except FileNotFoundError:
        print("❌ pactl command not found")
        return False


def list_pulse_sources():
    """List PulseAudio sources if available"""
    try:
        result = subprocess.run(
            ["pactl", "list", "short", "sources"], capture_output=True, text=True
        )
        if result.returncode == 0:
            print("\n🎤 PulseAudio Sources (Input Devices):")
            print("-" * 50)
            for line in result.stdout.strip().split("\n"):
                if line:
                    parts = line.split("\t")
                    if len(parts) >= 2:
                        source_id = parts[0]
                        source_name = parts[1]
                        print(f"  {source_id}: {source_name}")
                        if "wm8960" in source_name.lower() or "hw_2" in source_name:
                            print(f"    ⭐ This is your WM8960 device!")
            return True
    except:
        return False


def check_alsa_cards():
    """Check ALSA cards"""
    try:
        result = subprocess.run(["aplay", "-l"], capture_output=True, text=True)
        if result.returncode == 0:
            print("\n🎵 ALSA Cards:")
            print("-" * 50)
            print(result.stdout)
            return True
    except:
        return False


def get_current_defaults():
    """Get current default devices"""
    print("\n🎯 Current Default Devices:")
    print("-" * 50)

    # PulseAudio defaults
    try:
        result = subprocess.run(["pactl", "info"], capture_output=True, text=True)
        if result.returncode == 0:
            for line in result.stdout.split("\n"):
                if "Default Sink:" in line:
                    print(f"PulseAudio Default Sink: {line.split(':')[1].strip()}")
                elif "Default Source:" in line:
                    print(f"PulseAudio Default Source: {line.split(':')[1].strip()}")
    except:
        pass

    # Environment variables
    alsa_card = os.environ.get("ALSA_CARD")
    alsa_device = os.environ.get("ALSA_DEVICE")
    if alsa_card:
        print(f"ALSA_CARD environment: {alsa_card}")
    if alsa_device:
        print(f"ALSA_DEVICE environment: {alsa_device}")

    # PyAudio default
    try:
        import pyaudio

        audio = pyaudio.PyAudio()
        default_output = audio.get_default_output_device_info()
        print(
            f"PyAudio Default Output: Device {default_output['index']} - {default_output['name']}"
        )
        audio.terminate()
    except:
        print("Could not get PyAudio default device")


def provide_solutions():
    """Provide solutions based on detected audio system"""
    print("\n💡 Solutions to Set WM8960 as Default:")
    print("=" * 60)

    is_pulse = check_pulseaudio()

    if is_pulse:
        print("\n🎵 PulseAudio Solutions:")
        print("1. Find your WM8960 sink name from the list above")
        print("2. Set it as default temporarily:")
        print("   pactl set-default-sink alsa_output.hw_2_0")
        print("   # or use the exact sink name you see above")
        print("3. Run your script:")
        print("   python3 button_voice_assistant.py")
        print("4. Reset after (optional):")
        print("   pactl set-default-sink @DEFAULT_SINK@")

        print("\n🔄 One-liner approach:")
        print(
            "   pactl set-default-sink alsa_output.hw_2_0 && python3 button_voice_assistant.py"
        )

    else:
        print("\n🎵 Pure ALSA Solutions:")
        print("1. Using environment variables:")
        print("   ALSA_CARD=2 ALSA_DEVICE=0 python3 button_voice_assistant.py")
        print("2. Using card name:")
        print("   ALSA_CARD=wm8960soundcard python3 button_voice_assistant.py")
        print("3. Using the .asoundrc approach (permanent):")
        print("   python3 set_wm8960_default.py")


def main():
    print("🎧 Audio System Diagnostic Tool")
    print("=" * 50)

    check_pulseaudio()
    list_pulse_sinks()
    list_pulse_sources()
    check_alsa_cards()
    get_current_defaults()
    provide_solutions()


if __name__ == "__main__":
    main()
