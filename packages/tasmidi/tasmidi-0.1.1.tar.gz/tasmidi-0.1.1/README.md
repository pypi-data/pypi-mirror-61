# tasmidi

## What is this?

`tasmidi` is a collection of tools used to convert a LibTAS input file into a MIDI file. There are two steps to this: producing a mapping file to tell the program what notes correspond to what input, and using that mapping file to create the MIDI.

## Installation

```bash
pip install tasmidi
```

## How do I get the input file?

Assuming that your LibTAS movie file is called `tas-movie.ltm`:

```bash
tar xvzf tas-movie.ltm
```

This will produce several files, but the only one that we are interested in is called `inputs`.

## Usage

Both commands in this package have their own `--help` flag for specific usage. A typical workflow looks like:

```bash
tasmidi-map inputs > mapping.json # Generate a mapping file for the inputs
tasmidi-convert inputs -m mapping.json # Use that mapping and the input file to create a MIDI
```
