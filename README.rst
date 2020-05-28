
==================
Train Departure Pi
==================

..
.. sectnum::
    :depth: 1

.. contents:: **Contents**
    :depth: 1


Credits
  - Heavily inspired by `UK-Train-Departure-Display <https://github.com/ghostseven/UK-Train-Departure-Display>`_
    which forks `train-departure-screen <https://github.com/chrishutchinson/train-departure-screen>`_.

  - Font: `Dot-Matrix-Typeface <https://github.com/DanielHartUK/Dot-Matrix-Typeface>`_ by `Daniel Hart <https://github.com/DanielHartUK>`_.
  - Using the `Luma <https://github.com/rm-hull/luma.core>`_ library which provides a Pillow-compatible
    drawing canvas for the connected `SSD1322 Display <https://www.aliexpress.com/item/32949282762.html>`_

  - Used the `luma.examples <https://github.com/rm-hull/luma.examples>`_ repository's `CLI arguments parser <https://github.com/rm-hull/luma.examples/blob/master/examples/demo_opts.py>`_
    to initialise the different types of Luma devices.

Installation
============

Install dependencies with

.. code:: bash

    pip install -r requirements.txt

Run the pygame emulator with

.. code:: bash

    python ./src/main.py --display pygame --width 256 --height 64

Example departure board

.. image:: https://i.redd.it/hu788k5bih421.jpg
