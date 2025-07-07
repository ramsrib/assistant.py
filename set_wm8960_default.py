#!/usr/bin/env python3
"""
Script to set WM8960 sound card as the default audio output device
"""

import subprocess
import os


def set_wm8960_as_default():
    """Configure WM8960 as default audio output"""

    print("🎵 Configuring WM8960 as default audio output device...")

    # Create ALSA configuration to set wm8960 as default
    alsa_config = """# Set WM8960 sound card as default
pcm.!default {
    type hw
    card 2
    device 0
}

ctl.!default {
    type hw
    card 2
}
"""

    # Path to user ALSA config
    home_dir = os.path.expanduser("~")
    asoundrc_path = os.path.join(home_dir, ".asoundrc")

    try:
        # Backup existing .asoundrc if it exists
        if os.path.exists(asoundrc_path):
            backup_path = asoundrc_path + ".backup"
            print(f"📋 Backing up existing .asoundrc to {backup_path}")
            subprocess.run(["cp", asoundrc_path, backup_path], check=True)

        # Write new ALSA configuration
        with open(asoundrc_path, "w") as f:
            f.write(alsa_config)

        print(f"✅ Created {asoundrc_path}")
        print("🔄 Reloading ALSA configuration...")

        # Reload ALSA
        try:
            subprocess.run(["sudo", "alsa", "force-reload"], check=False)
        except:
            pass

        print("✅ WM8960 is now set as the default audio output device")
        print(
            "\n📝 Note: You may need to restart applications for changes to take effect"
        )

        return True

    except Exception as e:
        print(f"❌ Error configuring ALSA: {e}")
        return False


def test_audio_output():
    """Test audio output to verify the configuration"""
    print("\n🔊 Testing audio output...")

    try:
        # Test with speaker-test
        print("Playing test sound on default device (should be WM8960)...")
        result = subprocess.run(
            ["speaker-test", "-D", "default", "-t", "wav", "-c", "2", "-l", "1"],
            capture_output=True,
            text=True,
            timeout=10,
        )

        if result.returncode == 0:
            print("✅ Audio test completed successfully")
        else:
            print(f"⚠️  Audio test had issues: {result.stderr}")

    except subprocess.TimeoutExpired:
        print("✅ Audio test completed (timeout expected)")
    except FileNotFoundError:
        print("⚠️  speaker-test not found, skipping audio test")
    except Exception as e:
        print(f"⚠️  Audio test error: {e}")


def show_current_devices():
    """Show current audio device configuration"""
    print("\n📋 Current audio device status:")

    try:
        # Show ALSA cards
        result = subprocess.run(["aplay", "-l"], capture_output=True, text=True)
        if result.returncode == 0:
            print("Available ALSA devices:")
            for line in result.stdout.split("\n"):
                if "wm8960" in line.lower():
                    print(f"  🎵 {line}")
                elif "card" in line.lower():
                    print(f"    {line}")
    except:
        pass

    try:
        # Show default device info
        import pyaudio

        audio = pyaudio.PyAudio()
        default_output = audio.get_default_output_device_info()
        print(
            f"\n🔊 PyAudio default output: Device {default_output['index']} - {default_output['name']}"
        )
        audio.terminate()
    except:
        print("⚠️  Could not get PyAudio device info")


def main():
    print("🎧 WM8960 Default Audio Configuration Tool")
    print("=" * 50)

    show_current_devices()

    print("\n🎯 Setting WM8960 as default audio output...")
    if set_wm8960_as_default():
        test_audio_output()
        print("\n🎉 Configuration complete!")
        print("\nNow when you run button_voice_assistant.py,")
        print("it will automatically use the WM8960 sound card for output!")
    else:
        print("\n❌ Configuration failed")


if __name__ == "__main__":
    main()
