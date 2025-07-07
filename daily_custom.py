import asyncio
from daily import Daily, CallClient
import pyaudio


class DailyWithCustomAudio:
    def __init__(self):
        self.client = None
        self.input_device = None
        self.output_device = None

    def find_wm8960_devices(self):
        """Find WM8960 audio devices"""
        audio = pyaudio.PyAudio()

        input_device = None
        output_device = None

        print("Available audio devices:")
        for i in range(audio.get_device_count()):
            device_info = audio.get_device_info_by_index(i)
            name = device_info["name"].lower()

            print(f"  {i}: {device_info['name']}")
            print(f"     Input channels: {device_info['maxInputChannels']}")
            print(f"     Output channels: {device_info['maxOutputChannels']}")

            if "wm8960" in name or "soundcard" in name:
                if device_info["maxInputChannels"] > 0:
                    input_device = i
                    print(f"  → Found WM8960 input: {device_info['name']}")
                if device_info["maxOutputChannels"] > 0:
                    output_device = i
                    print(f"  → Found WM8960 output: {device_info['name']}")

        audio.terminate()
        return input_device, output_device

    async def setup_call(self, room_url, token=None):
        """Setup Daily call with custom audio devices"""

        # Find WM8960 devices
        self.input_device, self.output_device = self.find_wm8960_devices()

        if self.input_device is None or self.output_device is None:
            print("Warning: WM8960 devices not found, using defaults")

        # Create Daily client
        self.client = CallClient()

        # Configure audio settings
        audio_config = {
            "input": {
                "deviceId": str(self.input_device) if self.input_device else "default",
                "sampleRate": 44100,
                "channels": 2,
            },
            "output": {
                "deviceId": (
                    str(self.output_device) if self.output_device else "default"
                ),
                "sampleRate": 44100,
                "channels": 2,
            },
        }

        # Set up event handlers
        self.client.on("joined", self.on_joined)
        self.client.on("participant-joined", self.on_participant_joined)
        self.client.on("participant-left", self.on_participant_left)
        self.client.on("error", self.on_error)

        # Join the room
        await self.client.join(
            room_url,
            token,
            client_settings={
                "audio": audio_config,
                "video": False,  # Audio only for this example
            },
        )

    async def on_joined(self, data):
        print(f"Joined room: {data}")
        print(f"Using input device: {self.input_device}")
        print(f"Using output device: {self.output_device}")

    async def on_participant_joined(self, data):
        print(f"Participant joined: {data['participant']['user_name']}")

    async def on_participant_left(self, data):
        print(f"Participant left: {data['participant']['user_name']}")

    async def on_error(self, data):
        print(f"Error: {data}")

    async def leave_call(self):
        """Leave the Daily call"""
        if self.client:
            await self.client.leave()
            print("Left the call")


async def main():
    """Example usage"""

    # Your Daily room URL
    ROOM_URL = "https://test-project.daily.co/test-room"

    # Optional: meeting token for private rooms
    TOKEN = None  # or "your-meeting-token"

    daily_client = DailyWithCustomAudio()

    try:
        print("Setting up Daily call with WM8960...")
        await daily_client.setup_call(ROOM_URL, TOKEN)

        print("Connected! Press Enter to leave...")
        input()  # Wait for user input

    except Exception as e:
        print(f"Error: {e}")
    finally:
        await daily_client.leave_call()


if __name__ == "__main__":
    # Initialize Daily
    Daily.init()

    try:
        asyncio.run(main())
    finally:
        Daily.deinit()
