#!/bin/bash
# Wrapper script to run button_voice_assistant.py with WM8960 as default audio device
# This sets environment variables for the current session only - no permanent changes

echo "🎵 Running button voice assistant with WM8960 sound card..."
echo "   This is temporary - no permanent system changes"
echo ""

# Option 1: Using ALSA_CARD environment variable
echo "Setting ALSA_CARD=wm8960soundcard for this session..."
export ALSA_CARD=wm8960soundcard
export ALSA_DEVICE=0

# Show what we've set
echo "✅ Environment variables:"
echo "   ALSA_CARD=$ALSA_CARD"
echo "   ALSA_DEVICE=$ALSA_DEVICE"
echo ""

# Run the button assistant
echo "🚀 Starting button voice assistant..."
python3 button_voice_assistant.py

echo "👋 Session ended - audio settings reverted to normal" 