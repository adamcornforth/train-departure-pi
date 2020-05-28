# Train Departure Pi

Experiment with showing real-time train departure info via an SSD1322 OLED screen attached to a Raspberry Pi.

#### Credits:

- Heavily inspired by [UK-Train-Departure-Display](https://github.com/ghostseven/UK-Train-Departure-Display) which forks [train-departure-screen](https://github.com/chrishutchinson/train-departure-screen).
- Font: [Dot-Matrix-Typeface](https://github.com/DanielHartUK/Dot-Matrix-Typeface) by [Daniel Hart](https://github.com/DanielHartUK).
- Using the [Luma](https://github.com/rm-hull/luma.core) library which provides a Pillow-compatible drawing canvas for the connected [SSD1322 Display](https://www.aliexpress.com/item/32949282762.html)
- Used the [luma.examples](https://github.com/rm-hull/luma.examples) repository's [CLI arguments parser](https://github.com/rm-hull/luma.examples/blob/master/examples/demo_opts.py) to initialise the different types of Luma devices.

##  Installation

Install dependencies with 

`pip install -r requirements.txt`

Run the pygame emulator with

`python ./src/main.py --display pygame --width 256 --height 64`

![Emulator output](assets/emulator.png) ![Departure board](https://i.redd.it/hu788k5bih421.jpg)

## Hardware

The screen is a [SSD1322 chip OLED screen](https://www.aliexpress.com/item/32949282762.html).

### Notes on 4-SPI

The screen needs to be reconfigured to use 4SPI to work with the Luma library. From the comments in the Aliexpress link:

> The product arrived configured for protocol 8080. I unsoldered the resistance (R6) and I welded it on the support for the resistance in (R5) to use the 4SPI protocol

Also see [this blog post](https://www.balena.io/blog/build-a-raspberry-pi-powered-train-station-oled-sign-for-your-desk/#puttingittogether):

> Some displays have a solder-blob or zero-ohm resistor jumper on the back of the board that you may need to move in order to enable the display for SPI communication. If you don't get any output, check this first! In the case of my display it meant moving R6 to R5 to enable 4SPI as dictated by a small data table printed on the back of the display board.


### Schematic Diagram

These [schematics](https://ae01.alicdn.com/kf/H10b015a4b529447089d8d74d15d6c118T.jpg) show the pin-outs for the SSD1322 display.

Connections required to connect the display to the GPIO in the Raspberry Pi:

![Connections table](assets/display-to-pi-connections.png)