#!/usr/bin/env python3
"""
Fix PulseAudio to detect WM8960 or provide alternatives
"""

import subprocess
import os
import time


def restart_pulseaudio():
    """Restart PulseAudio to make it detect new devices"""
    print("🔄 Restarting PulseAudio to detect WM8960...")
    try:
        # Kill PulseAudio
        subprocess.run(["pulseaudio", "-k"], check=False)
        time.sleep(2)

        # Start PulseAudio
        subprocess.run(["pulseaudio", "--start"], check=True)
        time.sleep(3)

        print("✅ PulseAudio restarted")
        return True
    except Exception as e:
        print(f"❌ Error restarting PulseAudio: {e}")
        return False


def force_load_wm8960_module():
    """Force PulseAudio to load WM8960 module"""
    print("🎵 Loading WM8960 module in PulseAudio...")
    try:
        # Try to load the ALSA sink for card 2
        result = subprocess.run(
            [
                "pactl",
                "load-module",
                "module-alsa-sink",
                "device=hw:2,0",
                "sink_name=wm8960_output",
            ],
            capture_output=True,
            text=True,
        )

        if result.returncode == 0:
            print("✅ WM8960 sink loaded successfully!")
            return True
        else:
            print(f"❌ Failed to load WM8960 sink: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error loading module: {e}")
        return False


def force_load_wm8960_source():
    """Force PulseAudio to load WM8960 source (microphone)"""
    print("🎤 Loading WM8960 source in PulseAudio...")
    try:
        result = subprocess.run(
            [
                "pactl",
                "load-module",
                "module-alsa-source",
                "device=hw:2,0",
                "source_name=wm8960_input",
            ],
            capture_output=True,
            text=True,
        )

        if result.returncode == 0:
            print("✅ WM8960 source loaded successfully!")
            return True
        else:
            print(f"❌ Failed to load WM8960 source: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error loading source module: {e}")
        return False


def list_sinks_after_load():
    """List sinks after loading modules"""
    try:
        result = subprocess.run(
            ["pactl", "list", "short", "sinks"], capture_output=True, text=True
        )
        if result.returncode == 0:
            print("\n🔊 Available PulseAudio Sinks:")
            print("-" * 40)
            for line in result.stdout.strip().split("\n"):
                if line:
                    parts = line.split("\t")
                    if len(parts) >= 2:
                        sink_id = parts[0]
                        sink_name = parts[1]
                        print(f"  {sink_id}: {sink_name}")
                        if "wm8960" in sink_name.lower():
                            print(f"    ⭐ WM8960 detected!")
    except:
        pass


def set_wm8960_as_default():
    """Set WM8960 as default if it was loaded"""
    try:
        # Try to set wm8960_output as default
        result = subprocess.run(
            ["pactl", "set-default-sink", "wm8960_output"],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            print("✅ WM8960 set as default sink!")
            return True
        else:
            print("❌ Could not set WM8960 as default")
            return False
    except:
        return False


def bypass_pulseaudio_solution():
    """Provide solution to bypass PulseAudio entirely"""
    print("\n🎯 Alternative: Bypass PulseAudio Entirely")
    print("=" * 50)
    print("If PulseAudio module loading doesn't work, you can bypass PulseAudio:")
    print()
    print("1. Kill PulseAudio temporarily:")
    print("   pulseaudio -k")
    print()
    print("2. Run your script with direct ALSA:")
    print("   ALSA_CARD=2 python3 button_voice_assistant.py")
    print()
    print("3. Restart PulseAudio when done:")
    print("   pulseaudio --start")
    print()
    print("One-liner version:")
    print(
        "   pulseaudio -k && ALSA_CARD=2 python3 button_voice_assistant.py; pulseaudio --start"
    )


def main():
    print("🎧 PulseAudio WM8960 Fix Tool")
    print("=" * 40)

    print("\n🎯 Method 1: Force PulseAudio to detect WM8960")
    print("-" * 50)

    # Try to load WM8960 modules
    sink_loaded = force_load_wm8960_module()
    source_loaded = force_load_wm8960_source()

    if sink_loaded:
        list_sinks_after_load()
        if set_wm8960_as_default():
            print("\n🎉 Success! WM8960 is now the default PulseAudio sink")
            print("You can now run: python3 button_voice_assistant.py")
        else:
            print("\n⚠️  WM8960 loaded but couldn't set as default")
            print("Try: pactl set-default-sink wm8960_output")
    else:
        print("\n❌ Could not load WM8960 module in PulseAudio")
        bypass_pulseaudio_solution()


if __name__ == "__main__":
    main()
