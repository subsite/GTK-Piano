# GTK Piano

A simple piano app vibe coded in 1h because I needed one right now. Tested on Arch and Ubuntu Linux. 

## Install and run

Install `gtk3`, then:

```sh
git clone https://github.com/subsite/GTK-Piano.git
cd GTK-Piano
chmod +x run.sh
./run.sh
```

## Create system shortcut
Create the file `~/.local/share/applications/gtk-piano.desktop`:

```
[Desktop Entry]
Name=GTK Piano
Exec=/path/to/repo/GTK-piano/run.sh
Icon=/path/to/repo/GTK-piano/piano.png
Type=Application
Categories=Audio;
```

### Piano sound:
https://www.zanderjaz.com/downloads/soundfonts/pianos/




## Audio driver

The default is ALSA. Override with e.g. `PIANO_AUDIO_DRIVER=pulseaudio ./run.sh` (or `pipewire`).

If you get `module 'fluidsynth' has no attribute 'Synth'`, an unrelated `fluidsynth` pip package shadows `pyfluidsynth`. Delete `venv/` and run `./run.sh` again. `pyfluidsynth` also needs the system FluidSynth library (Arch: `fluidsynth`, Ubuntu: `libfluidsynth3`, Fedora: `fluidsynth-libs`).

## Flatpak

Download `gtk-piano.flatpak` from the latest GitHub release, then:

```sh
flatpak install --user gtk-piano.flatpak
flatpak run io.github.subsite.GTKPiano
```

### Building locally

```sh
flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
flatpak install flathub org.gnome.Platform//49 org.gnome.Sdk//49
flatpak-builder --install --user build-dir flatpak/io.github.subsite.GTKPiano.yml
```

### Releasing

Enable the auto-tag hook once: `git config core.hooksPath .githooks`

1. Bump `VERSION`
2. Add a `<release>` entry in `flatpak/io.github.subsite.GTKPiano.metainfo.xml`
3. Commit: `git commit -am "release 1.1.0"`. The post-commit hook creates the `v1.1.0` tag
4. Push: `git push origin main --tags`

GitHub Actions picks up the tag, builds the `.flatpak` bundle, and publishes a GitHub release.
