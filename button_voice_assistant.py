#!/usr/bin/env python3
"""
Button-triggered voice assistant on Raspberry Pi
Press the button to toggle VAPI calls (start/stop)
Uses system default audio device (configure with set_wm8960_default.py)
LED on GPIO25 blinks when call is active
"""

import os
import threading
import time
from gpiozero import Button, LED
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

api_key = os.getenv("VAPI_API_KEY")
assistant_id = os.getenv("VAPI_ASSISTANT_ID")

# Hardware setup (GPIO pins from NOTES.md)
button = Button(23)  # Button on GPIO23
led = LED(25)  # LED on GPIO25

# Global VAPI instance and call state
vapi_client = None
call_active = False
led_thread = None
led_stop_event = threading.Event()


def led_blink_pattern():
    """LED blinking pattern while call is active"""
    while not led_stop_event.is_set():
        if call_active:
            led.on()
            time.sleep(0.5)  # LED on for 0.5 seconds
            if not led_stop_event.is_set():
                led.off()
                time.sleep(0.5)  # LED off for 0.5 seconds
        else:
            led.off()
            break


def start_led_blinking():
    """Start LED blinking in a separate thread"""
    global led_thread, led_stop_event

    # Stop any existing blinking
    stop_led_blinking()

    # Start new blinking thread
    led_stop_event.clear()
    led_thread = threading.Thread(target=led_blink_pattern, daemon=True)
    led_thread.start()
    print("💡 LED blinking started")


def stop_led_blinking():
    """Stop LED blinking and turn off LED"""
    global led_thread, led_stop_event

    if led_thread and led_thread.is_alive():
        led_stop_event.set()
        led_thread.join(timeout=1.0)

    led.off()
    print("💡 LED turned off")


def initialize_vapi():
    """Initialize VAPI client"""
    global vapi_client
    try:
        from vapi_python import Vapi

        vapi_client = Vapi(api_key=api_key)
        print("✅ VAPI client initialized successfully")
        print(
            "🔊 Audio output will use system default device (configure with set_wm8960_default.py)"
        )
        return True
    except ImportError as e:
        print(f"❌ Error: Missing dependency for local vapi_python.py: {e}")
        print("   Make sure 'daily-python' is installed: pip install daily-python")
        return False
    except Exception as e:
        print(f"❌ Error initializing VAPI: {e}")
        return False


def start_vapi_call():
    """Start a VAPI call using the client library"""
    global vapi_client, call_active

    if not vapi_client:
        print("❌ VAPI client not initialized")
        return

    if not assistant_id:
        print("❌ VAPI_ASSISTANT_ID not set in environment variables")
        return

    try:
        print(f"🎙️  Starting VAPI call with assistant_id: {assistant_id}")
        vapi_client.start(assistant_id=assistant_id)
        call_active = True
        start_led_blinking()  # Start LED blinking when call starts
        print("📞 Call started successfully!")
    except Exception as e:
        print(f"❌ Error starting call: {e}")


def stop_vapi_call():
    """Stop the current VAPI call"""
    global vapi_client, call_active

    if not vapi_client:
        print("❌ VAPI client not initialized")
        return

    try:
        vapi_client.stop()
        call_active = False
        stop_led_blinking()  # Stop LED blinking when call stops
        print("📴 Call stopped")
    except Exception as e:
        print(f"❌ Error stopping call: {e}")
        call_active = False  # Reset state even if there's an error
        stop_led_blinking()  # Ensure LED is turned off even on error


def on_button_press():
    """Handle button press event - toggle call on/off"""
    global call_active

    if call_active:
        print("🔘 Button pressed! Call active - stopping voice assistant...")
        stop_vapi_call()
    else:
        print("🔘 Button pressed! No active call - starting voice assistant...")
        start_vapi_call()


def on_button_release():
    """Handle button release event (optional - can stop the call)"""
    print("🔘 Button released! Stopping voice assistant...")
    stop_vapi_call()


def main():
    print("🚀 Button-triggered voice assistant on Raspberry Pi")

    # Check environment variables
    if not api_key:
        print("❌ VAPI_API_KEY not set in environment variables")
        return

    if not assistant_id:
        print("❌ VAPI_ASSISTANT_ID not set in environment variables")
        return

    print(f"✅ Environment check passed")
    print(
        f"   VAPI_API_KEY: {api_key[:10]}..." if api_key else "   VAPI_API_KEY: Not set"
    )
    print(f"   VAPI_ASSISTANT_ID: {assistant_id}")

    # Initialize VAPI client
    if not initialize_vapi():
        return

    # Set up button events
    button.when_pressed = on_button_press
    # Uncomment the next line if you want to stop the call when button is released
    # button.when_released = on_button_release

    print("\n🎯 Ready! Press the button on GPIO23 to toggle voice assistant")
    print("   First press: Start call | Second press: Stop call")
    print("   💡 LED on GPIO25 will blink when call is active")
    print("   Audio uses system default device")
    print("   Press CTRL+C to exit")

    try:
        # Keep the script running
        while True:
            pass
    except KeyboardInterrupt:
        print("\n👋 Exiting...")
        if vapi_client and call_active:
            stop_vapi_call()
        stop_led_blinking()  # Ensure LED is turned off on exit


if __name__ == "__main__":
    main()
