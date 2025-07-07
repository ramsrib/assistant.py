# NOTES

[Push button is connected to GPIO 23 and the led GPIO25](https://forum.raspiaudio.com/t/ultra-installation-guide/21), so it is of course optional but if you write a program is could be used to perform some actions (recording for example) without the need of using a keyboard.

There are many controls with the ULTRA and it could be confusing at first. So we have made some ALSA script so you can autoconfigure it to for example [preset_external_jack_microphone_input2 11](https://raw.githubusercontent.com/RASPIAUDIO/WM8960-Audio-HAT/master/preset_external_jack_microphone_input2)

to enable the microphone input see [here for tutorial](https://forum.raspiaudio.com/t/ultra-installation-guide/21)

### Features

**Inputs:**

**Onboard microphone Left, RightJack stereo microphoneJack stereo line inputUser push button**

- Onboard microphone Left, Right
- Jack stereo microphone
- Jack stereo line input
- User push button

**Outputs:**

**2w onboard stereo spakers (pre-soldered)2w output stereo for external speakersHeadphone jack stereoUser led**

- 2w onboard stereo spakers (pre-soldered)
- 2w output stereo for external speakers
- Headphone jack stereo
- User led

**Features:**

**NEW! Plug and play automatic driver installation thanks to the integrated Eeprom!65x30x15mm (compact Raspberry pi Zero format=Compatible with raspberry 5 rp4  (all version), Raspberry 3 (all versions), Zero (all versions)Standard Raspberry Pi 40PIN GPIO extension header, supports Raspberry Pi series boardsIntegrates WM8960 low power stereo CODEC, communicates via I2S interfaceIntegrates dual high-quality MEMS silicon Mic, supports left & right double channels recording, nice sound qualityOnboard standard 3.5mm earphone jack, play music via external earphoneOnboard dual-channel speaker interface, directly drives speakersSupports sound effects such as stereo, 3D surrounding, etc.Headphone output (24bits) WM8960input / output MixerHardware volume control24 Bit I2S Dac2×1.3W Stereo Amplifier for external speakersStereo onbard speakers2 Onboard microphonesStereo 3.5mm LINE jack inputStereo 3.5mm MICROPHONE jack input**

- **NEW! Plug and play automatic driver installation thanks to the integrated Eeprom!**
- 65x30x15mm (compact Raspberry pi Zero format=
- Compatible with raspberry 5 rp4 (all version), Raspberry 3 (all versions), Zero (all versions)
- Standard Raspberry Pi 40PIN GPIO extension header, supports Raspberry Pi series boards
- Integrates WM8960 low power stereo CODEC, communicates via I2S interface
- Integrates dual high-quality MEMS silicon Mic, supports left & right double channels recording, nice sound quality
- Onboard standard 3.5mm earphone jack, play music via external earphone
- Onboard dual-channel speaker interface, directly drives speakers
- Supports sound effects such as stereo, 3D surrounding, etc.
- Headphone output (24bits) WM8960
- input / output Mixer
- Hardware volume control
- 24 Bit I2S Dac
- 2×1.3W Stereo Amplifier for external speakers
- Stereo onbard speakers
- 2 Onboard microphones
- Stereo 3.5mm LINE jack input
- Stereo 3.5mm MICROPHONE jack input

**CODEC: WM8960Power supply: 5VLogic voltage: 3.3VControl interface: I2CAudio interface: I2SDAC signal-noise ratio: 98dBADC signal-noise ratio: 94dBEarphone driver: 40mW (16Ω@3.3V)Speaker driver: 1.3W per channel (8Ω BTL)**

- CODEC: WM8960
- Power supply: 5V
- Logic voltage: 3.3V
- Control interface: I2C
- Audio interface: I2S
- DAC signal-noise ratio: 98dB
- ADC signal-noise ratio: 94dB
- Earphone driver: 40mW (16Ω@3.3V)
- Speaker driver: 1.3W per channel (8Ω BTL)

**Device number**

*this will be usefull in the alsa mixer to understand what input is connected to which microphones*

Onbard microphones:

Linput1

Rinput1

External microphone jack input:

Linput2

Rinput2

Line input

Linput3

Rinput3

External speakers/speaker output:

SPK_L

SPK_R

**Pinout:**

| GPIO | PIN | FUNCTION |
| --- | --- | --- |
| GPIO2 | PIN3 | I2C SDA |
| GPIO3 | PIN5 | I2C SCL |
| GPIO25 | PIN22 | LED |
|  | PIN17 | 3.3v |
|  | PIN25 39 6 14 | GND |
| GPIO19 | PIN35 | I2S LRCLK |
|  | PIN2 4 | 5v |
| GPIO18 | PIN12 | I2S CLK |
| GPIO20 | PIN38 | I2S ADC |
| GPIO21 | PIN40 | I2S DAC |
| GPIO23 | PIN16 | BUTTON (this pin as an external pull up) |

## References

[https://www.amazon.com/dp/B08HVQQSWP](https://www.amazon.com/dp/B08HVQQSWP?tag=goodswave08-20&th=1)

<https://raspiaudio.com/product/ultra/>

<https://forum.raspiaudio.com/t/ultra-installation-guide/21>
