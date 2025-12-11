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




