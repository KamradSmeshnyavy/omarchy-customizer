# Omarchy Customizer

[🇷🇺 Русский](README.ru.md)

One overlay for the whole look & feel of [Omarchy](https://omarchy.org): themes, wallpapers, Hyprland
animations, transparency, blur and screen shaders — with live preview while you browse. With the companion
plugins installed it also drives the bar, the lock screen, wallpaper transitions and the picker style.

![Desktop](screenshots/desktop.webp)

| Group | What's inside |
|---|---|
| **Desktop** | Theme (palette + preview), Wallpaper (categories as in the background switcher), Recolor (any image into the current theme with lutgen), Wallpaper FX* |
| **Bar*** | Bar Skin, Bar Layout, Bar Tweaks — 41 settings, each with its default and a live preview |
| **Windows** | Animations (17 presets), Transparency, Blur, Shader (CRT / TFT) — all live while you browse |
| **Lock*** | Lock design with previews in the current theme, Lock Tweaks |
| **Pickers*** | Theme / wallpaper picker style, thumbnail cache |

\* appears only when the matching companion plugin is installed — see below.

| Bar | Windows |
| :---: | :---: |
| ![Bar](screenshots/bar.webp) | ![Windows](screenshots/windows.webp) |
| **Lock** | **Pickers** |
| ![Lock](screenshots/lock.webp) | ![Pickers](screenshots/pickers.webp) |

## Install

Customizer, plus a question for each companion plugin:

```sh
curl -fsSL https://raw.githubusercontent.com/KamradSmeshnyavy/omarchy-customizer/main/install.sh | bash
```

`… | bash -s -- --all` installs every companion, `--with bar,lock` only the listed ones, `--none` just the
Customizer. The script adds each plugin with `omarchy plugin add`, binds **Super+Shift+T** in
`~/.config/hypr/bindings.lua` and restarts the shell.

By hand:

```sh
omarchy plugin add https://github.com/KamradSmeshnyavy/omarchy-customizer --enable
omarchy restart shell
```

and bind it in `~/.config/hypr/bindings.lua`:

```lua
o.bind("SUPER + SHIFT + T", "Omarchy Customizer", "omarchy-shell shell toggle kamradsmeshnyavy.customizer")
```

Tested on Omarchy 4.0.6 with Quickshell 0.3.2.

### Companion plugins

Each is a separate plugin; the Customizer finds them on its own.

| Plugin | Adds to the Customizer |
|---|---|
| [omarchy-bar-skins](https://github.com/KamradSmeshnyavy/omarchy-bar-skins) | **Bar** group: 18 skins, 9 layouts, compact mode, workspace styles |
| [omarchy-lock-designs](https://github.com/KamradSmeshnyavy/omarchy-lock-designs) | **Lock** group: 21 designs |
| [omarchy-wallpaper-fx](https://github.com/KamradSmeshnyavy/omarchy-wallpaper-fx) | **Wallpaper FX**: 24 transitions with a preview |
| [omarchy-image-picker-styles](https://github.com/KamradSmeshnyavy/omarchy-image-picker-styles) | **Pickers** group: six picker styles |
| [omarchy-launcher-skins](https://github.com/KamradSmeshnyavy/omarchy-launcher-skins) | full-screen launcher skins (configured in its own file) |

### Optional programs

- `libvips` — fast thumbnails for themes and wallpapers (`omarchy pkg add libvips`)
- `zenity` — dialogs for colours, text and files in the tweaks
- `lutgen` — Recolor (shown only when both lutgen and zenity are there)

## Keys

| Keys | |
|---|---|
| Tab / 1–5 | groups |
| j k · l ⏎ · h | move · open · back |
| / | search |
| h l, − + | change a tweak · x — reset it |
| p | play / show live (transitions, lock designs, picker) |
| r | surprise me |
| ? · q / Esc | all keys · close |

## How your choices survive a reload

The animation preset goes to `~/.local/state/omarchy-customizer/animations.lua`; transparency, blur and the
shader go to `~/.local/state/hypr/{opacity,blur,screen-shader}`. The Customizer re-applies them when the
shell starts and after every `hyprctl reload`. For a reload without even a flash of the defaults, load the
hook from your Hyprland config (e.g. at the end of `~/.config/hypr/looknfeel.lua`):

```lua
dofile(os.getenv("HOME") .. "/.config/omarchy/plugins/kamradsmeshnyavy.customizer/hypr/customizer.lua")
```

The scripts work on their own too — bind them if you like:

```lua
o.bind("SUPER + ALT + O", "Next transparency preset", "~/.config/omarchy/plugins/kamradsmeshnyavy.customizer/scripts/opacity.sh next")
o.bind("SUPER + ALT + U", "Next blur preset", "~/.config/omarchy/plugins/kamradsmeshnyavy.customizer/scripts/blur.sh next")
o.bind("SUPER + ALT + C", "Toggle screen shader", "~/.config/omarchy/plugins/kamradsmeshnyavy.customizer/scripts/crt-toggle.sh")
```

## Your own presets

- Animations: `~/.config/omarchy/customizer/animations/*.lua` (Hyprland Lua: `hl.curve`, `hl.animation`).
  A file with the same name as a bundled preset replaces it.
- Shaders: `~/.config/omarchy/customizer/shaders/*.frag`. A shader that uses `time` gets
  `damage_tracking = 0` automatically, a warping one `1`.

## Language

English and Russian. The language comes from `"lang"` in `~/.config/omarchy/customizer.json`, otherwise
from `$LANG` (`ru*` → Russian). Translations live in `i18n/<lang>.json`: the English string is the key —
a new language is one more file.

## License

GPL-3.0 — see [LICENSE](LICENSE) and [NOTICE](NOTICE). The animation presets come from
[HyDE](https://github.com/HyDE-Project/HyDE), [ML4W](https://github.com/mylinuxforwork/dotfiles) and
[end-4](https://github.com/end-4/dots-hyprland) ([credits](animations/CREDITS.md)); the overlay follows the
style of [Omarchy](https://github.com/basecamp/omarchy)'s own shell plugins (MIT).

Part of [my dotfiles](https://github.com/KamradSmeshnyavy/dotfiles).
