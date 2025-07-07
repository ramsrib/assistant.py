#!/usr/bin/env python3
"""
WM8960 Volume Control Tool
Control volume for WM8960 sound card through PulseAudio
"""

import subprocess
import sys


def get_current_volume():
    """Get current volume of wm8960_output sink"""
    try:
        result = subprocess.run(
            ["pactl", "get-sink-volume", "wm8960_output"],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            print(f"🔊 Current WM8960 Volume: {result.stdout.strip()}")
            return True
        else:
            print("❌ Could not get volume")
            return False
    except Exception as e:
        print(f"❌ Error getting volume: {e}")
        return False


def set_volume(volume_percent):
    """Set volume for wm8960_output sink"""
    try:
        # Ensure volume is between 0-150% (PulseAudio allows up to 150%)
        volume_percent = max(0, min(150, volume_percent))

        result = subprocess.run(
            ["pactl", "set-sink-volume", "wm8960_output", f"{volume_percent}%"],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            print(f"✅ WM8960 volume set to {volume_percent}%")
            return True
        else:
            print(f"❌ Could not set volume: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error setting volume: {e}")
        return False


def mute_sink():
    """Mute the wm8960_output sink"""
    try:
        result = subprocess.run(
            ["pactl", "set-sink-mute", "wm8960_output", "1"],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            print("🔇 WM8960 muted")
            return True
        else:
            print("❌ Could not mute")
            return False
    except Exception as e:
        print(f"❌ Error muting: {e}")
        return False


def unmute_sink():
    """Unmute the wm8960_output sink"""
    try:
        result = subprocess.run(
            ["pactl", "set-sink-mute", "wm8960_output", "0"],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            print("🔊 WM8960 unmuted")
            return True
        else:
            print("❌ Could not unmute")
            return False
    except Exception as e:
        print(f"❌ Error unmuting: {e}")
        return False


def volume_up(step=10):
    """Increase volume by step amount"""
    try:
        result = subprocess.run(
            ["pactl", "set-sink-volume", "wm8960_output", f"+{step}%"],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            print(f"🔊 Volume increased by {step}%")
            get_current_volume()
            return True
        else:
            print("❌ Could not increase volume")
            return False
    except Exception as e:
        print(f"❌ Error increasing volume: {e}")
        return False


def volume_down(step=10):
    """Decrease volume by step amount"""
    try:
        result = subprocess.run(
            ["pactl", "set-sink-volume", "wm8960_output", f"-{step}%"],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            print(f"🔉 Volume decreased by {step}%")
            get_current_volume()
            return True
        else:
            print("❌ Could not decrease volume")
            return False
    except Exception as e:
        print(f"❌ Error decreasing volume: {e}")
        return False


def show_help():
    """Show available commands"""
    print("🎧 WM8960 Volume Control Commands")
    print("=" * 40)
    print()
    print("📊 Get current volume:")
    print("   python3 wm8960_volume_control.py status")
    print("   # or")
    print("   pactl get-sink-volume wm8960_output")
    print()
    print("🔊 Set specific volume (0-150%):")
    print("   python3 wm8960_volume_control.py set 75")
    print("   # or")
    print("   pactl set-sink-volume wm8960_output 75%")
    print()
    print("🔊 Volume up/down:")
    print("   python3 wm8960_volume_control.py up")
    print("   python3 wm8960_volume_control.py down")
    print("   # or")
    print("   pactl set-sink-volume wm8960_output +10%")
    print("   pactl set-sink-volume wm8960_output -10%")
    print()
    print("🔇 Mute/Unmute:")
    print("   python3 wm8960_volume_control.py mute")
    print("   python3 wm8960_volume_control.py unmute")
    print("   # or")
    print("   pactl set-sink-mute wm8960_output 1    # mute")
    print("   pactl set-sink-mute wm8960_output 0    # unmute")
    print()
    print("💡 Quick Examples:")
    print("   pactl set-sink-volume wm8960_output 50%   # Set to 50%")
    print("   pactl set-sink-volume wm8960_output +5%   # Increase by 5%")
    print("   pactl set-sink-volume wm8960_output -5%   # Decrease by 5%")


def main():
    if len(sys.argv) < 2:
        print("🎧 WM8960 Volume Control")
        print("Usage: python3 wm8960_volume_control.py <command> [value]")
        print("Commands: status, set, up, down, mute, unmute, help")
        sys.exit(1)

    command = sys.argv[1].lower()

    if command == "status":
        get_current_volume()
    elif command == "set":
        if len(sys.argv) < 3:
            print("❌ Please specify volume level (0-150)")
            sys.exit(1)
        try:
            volume = int(sys.argv[2])
            set_volume(volume)
        except ValueError:
            print("❌ Volume must be a number")
            sys.exit(1)
    elif command == "up":
        step = 10
        if len(sys.argv) >= 3:
            try:
                step = int(sys.argv[2])
            except ValueError:
                pass
        volume_up(step)
    elif command == "down":
        step = 10
        if len(sys.argv) >= 3:
            try:
                step = int(sys.argv[2])
            except ValueError:
                pass
        volume_down(step)
    elif command == "mute":
        mute_sink()
    elif command == "unmute":
        unmute_sink()
    elif command == "help":
        show_help()
    else:
        print(f"❌ Unknown command: {command}")
        print("Available commands: status, set, up, down, mute, unmute, help")
        sys.exit(1)


if __name__ == "__main__":
    main()
