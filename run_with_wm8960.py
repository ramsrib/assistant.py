#!/usr/bin/env python3
"""
Wrapper script to run button_voice_assistant.py with WM8960 as default audio device
This sets environment variables for the current session only - no permanent changes
"""

import os
import subprocess
import sys


def set_audio_environment():
    """Set environment variables to use WM8960 as default"""

    print("🎵 Setting WM8960 as default audio device for this session...")

    # Set ALSA environment variables
    env = os.environ.copy()

    # Option 1: Set ALSA card directly
    env["ALSA_CARD"] = "wm8960soundcard"  # or just '2'

    # Option 2: Alternative - set ALSA device
    env["ALSA_DEVICE"] = "0"

    # Option 3: Set default ALSA config in memory
    env["ALSA_CONFIG_PATH"] = "/dev/null"  # Ignore system config

    print("✅ Environment variables set:")
    print(f"   ALSA_CARD = {env.get('ALSA_CARD')}")
    print(f"   ALSA_DEVICE = {env.get('ALSA_DEVICE')}")

    return env


def run_button_assistant():
    """Run the button voice assistant with WM8960 environment"""

    env = set_audio_environment()

    print("\n🚀 Starting button voice assistant with WM8960...")
    print("   This will only affect this session - no permanent changes")
    print("   Press CTRL+C to exit\n")

    try:
        # Run the button assistant with modified environment
        result = subprocess.run([sys.executable, "button_voice_assistant.py"], env=env)

        return result.returncode

    except KeyboardInterrupt:
        print("\n👋 Session ended")
        return 0
    except Exception as e:
        print(f"❌ Error running button assistant: {e}")
        return 1


def show_audio_options():
    """Show different ways to set audio device temporarily"""

    print("🎧 Temporary Audio Device Configuration Options")
    print("=" * 60)
    print()
    print("Option 1: Environment Variables (this script)")
    print("   python3 run_with_wm8960.py")
    print()
    print("Option 2: Direct ALSA_CARD environment variable")
    print("   ALSA_CARD=wm8960soundcard python3 button_voice_assistant.py")
    print("   # or")
    print("   ALSA_CARD=2 python3 button_voice_assistant.py")
    print()
    print("Option 3: PulseAudio (if using pulse)")
    print("   pactl set-default-sink alsa_output.hw_2_0")
    print("   python3 button_voice_assistant.py")
    print("   pactl set-default-sink @DEFAULT_SINK@  # reset after")
    print()
    print("Option 4: ALSA config override")
    print('   ALSA_CONFIG_UCM2_DIR="/tmp" python3 button_voice_assistant.py')
    print()


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        show_audio_options()
    else:
        exit_code = run_button_assistant()
        sys.exit(exit_code)
