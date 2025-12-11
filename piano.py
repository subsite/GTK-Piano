#!/usr/bin/env python3

import sys, gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GLib
import fluidsynth

# ----- Fluidsynth setup -----
fs = fluidsynth.Synth(samplerate=44100)
fs.start(driver="alsa")  # or "pulseaudio" if needed

sfid = fs.sfload("./Stein_Grand_Piano.sf2")
fs.program_select(0, sfid, 0, 0)  # channel 0, bank 0, program 0

fs.cc(0, 7, 0)
GLib.timeout_add(50, lambda: fs.cc(0, 7, 100) or False)

fs.setting("synth.reverb.active", 1)       
fs.setting("synth.reverb.level", 0.6)      
fs.setting("synth.reverb.room-size", 0.6)  


def note_on(midi):
    fs.noteon(0, midi, 100)

def note_off(midi):
    fs.noteoff(0, midi)

# ----- Piano UI -----
BLACKS = {1, 3, 6, 8, 10}
MIDI_START = 36         # C4
NUM_NOTES = 49          # 3 octaves

KEY_WIDTH = 44
WHITE_HEIGHT = 220
BLACK_HEIGHT = 130
BLACK_WIDTH = 28

# black key offsets in one octave (relative to C white key)
BLACK_OFFSETS = {1:0.65, 3:1.65, 6:3.65, 8:4.65, 10:5.65}

class PianoWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="GTK Piano")
        self.set_border_width(8)
        self.set_resizable(False)
        self.set_default_icon_from_file("./piano.png")

        keyboard = Gtk.Fixed()
        self.add(keyboard)

        num_octaves = NUM_NOTES // 12
        white_x = 0

        # Create white keys
        for i in range(NUM_NOTES):
            midi = MIDI_START + i
            semitone = midi % 12
            if semitone not in BLACKS:
                w = Gtk.Button()
                w.set_size_request(KEY_WIDTH, WHITE_HEIGHT)
                w.get_style_context().add_class("white-key")
                w.connect("pressed", self.on_press, midi)
                w.connect("released", self.on_release, midi)
                keyboard.put(w, white_x, 0)
                white_x += KEY_WIDTH

        # Create black keys
        for octave in range(num_octaves):
            base_x = octave * 7 * KEY_WIDTH
            for semitone in BLACKS:
                midi = MIDI_START + octave * 12 + semitone
                blk = Gtk.Button()
                blk.set_size_request(BLACK_WIDTH, BLACK_HEIGHT)
                blk.get_style_context().add_class("black-key")
                blk.connect("pressed", self.on_press, midi)
                blk.connect("released", self.on_release, midi)
                x = int(base_x + BLACK_OFFSETS[semitone] * KEY_WIDTH)
                keyboard.put(blk, x, 0)

        css = b"""
            .white-key { background: #fff; border: 1px solid #000; }
            .white-key:active { background: #ccc; }
            .black-key { background: #000; color: #fff; }
            .black-key:active { background: #555; }
        """
        provider = Gtk.CssProvider()
        provider.load_from_data(css)
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        self.connect("destroy", Gtk.main_quit)

    def on_press(self, widget, midi):
        note_on(midi)

    def on_release(self, widget, midi):
        note_off(midi)

def main():
    win = PianoWindow()
    win.set_default_size(7 * KEY_WIDTH * (NUM_NOTES // 12) + 40, WHITE_HEIGHT + 60)
    win.show_all()
    Gtk.main()
    fs.delete()

if __name__ == "__main__":
    main()
