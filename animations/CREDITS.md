# Animation presets — credits

Every preset here is a Hyprland animation config converted to the Lua config format. They come from
projects licensed under GPL-3.0:

| Presets | Source |
|---|---|
| `00-default`, `01-default - v2`, `03- Disable Animation` | [HyDE](https://github.com/HyDE-Project/HyDE) (`01-default`, `00-disable`) |
| `HYDE - default`, `HYDE - minimal-1`, `HYDE - minimal-2`, `HYDE - optimized`, `HYDE - Vertical` | [HyDE](https://github.com/HyDE-Project/HyDE) |
| `Mahaveer - me-1`, `Mahaveer - me-2` | [HyDE](https://github.com/HyDE-Project/HyDE) (`me-1`, `me-2`, by Mahaveer) |
| `END-4` | [end-4/dots-hyprland](https://github.com/end-4/dots-hyprland) |
| `ML4W - classic`, `ML4W - dynamic`, `ML4W - fast`, `ML4W - high`, `ML4W - moving`, `ML4W - standard` | [ML4W dotfiles](https://github.com/mylinuxforwork/dotfiles) |
| `DOT-MATRIX` | [Nihil-Shell](https://github.com/poligle/Nihil-Shell) (MIT, by Pol Iglesias) |
| `yami` | after [yami](https://github.com/Trendorin/yami) (MIT): the durations and curves of its niri animations; its pixel dissolve shaders have no Hyprland equivalent |
| `rumda` | after [Rumda](https://github.com/hexonide/rumda): the durations and curves of its hyprland.conf animations |
| `surface` | from [surface-dots](https://github.com/snes19xx/surface-dots) by snes19xx (its README allows reuse with credit): the Material 3 curves and the window springs of its hyprland.lua |
| `cozytile` | after [Cozytile](https://github.com/Darkkal44/Cozytile) (no licence — the feel only): its picom fades, ≈ 165 ms, windows appear and vanish in place |
| `bruteon` | after [Bruteon](https://github.com/Darkkal44/Bruteon) (screenshots only — own feel): quick springy pop-ins of windows and layers |
| `unit3` | from [Unit-3](https://github.com/samyns/Unit-3) by samyns (MIT): its `niercurve` bezier — windows slide in / out, workspaces slide vertically |
| `space` | from the Space style of [elifouts/Dotfiles](https://github.com/elifouts/Dotfiles) (GPL-3.0): its `style.lua` — windows pop in on the `easy` spring, quick fades, layers and workspaces on `easeOutQuint` |
| `crt` | from the Retro style of [elifouts/Dotfiles](https://github.com/elifouts/Dotfiles) (GPL-3.0): its `style.lua` — everything on the sharp `snap` curve, windows pop in at 96 % and close on a `step`, workspaces slide-fade 8 % |
| `modern` | from the Modern style of [elifouts/Dotfiles](https://github.com/elifouts/Dotfiles) (GPL-3.0): its `style.lua` — windows pop in 5 % on the `fluid` curve, close and fade on `snappy`, workspaces slide, layers pop in 70 % |

Add your own presets to `~/.config/omarchy/customizer/animations/*.lua`: they show up in the list, and a
file with the same name overrides the bundled one.
