#!/usr/bin/env python3
"""
Voice assistant on Raspberry Pi
"""

import os
import numpy as np
from dotenv import load_dotenv

# client sdk
# from vapi_python import Vapi

# server sdk
# from vapi import Vapi

# Load environment variables
load_dotenv()

api_key = os.getenv("VAPI_API_KEY")
assistant_id = os.getenv("VAPI_ASSISTANT_ID")


def create_server_call():

    print(f"Creating call with assistant_id: {assistant_id}")
    from vapi import Vapi

    vapi = Vapi(token=api_key)
    # Create an outbound call
    call = vapi.calls.create(
        phone_number_id="YOUR_PHONE_NUMBER_ID",
        customer={"number": "+1234567890"},
        assistant_id=assistant_id,
    )
    print(f"Call created: {call.id}")


def create_client_call():
    print(f"Creating call with assistant_id: {assistant_id}")
    from vapi_python import Vapi

    vapi = Vapi(api_key=api_key)
    vapi.start(assistant_id=assistant_id)
    # vapi.stop()


def main():
    print("🚀 Voice assistant on Raspberry Pi")

    # Check for environment variables
    api_key = os.getenv("VAPI_API_KEY", "Not set")
    print(f"\nEnvironment check - VAPI_API_KEY: {api_key}")


if __name__ == "__main__":
    main()
    create_client_call()
