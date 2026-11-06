#!/bin/sh
# ALSA isn't reachable from the sandbox; go through the pulseaudio socket
export PIANO_AUDIO_DRIVER="${PIANO_AUDIO_DRIVER:-pulseaudio}"
exec python3 /app/share/gtk-piano/piano.py "$@"
