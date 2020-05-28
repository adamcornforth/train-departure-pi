# Train Departure Pi

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

Example departure board

![img](https://i.redd.it/hu788k5bih421.jpg)
