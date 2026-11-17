"""Динамическая тема райса: вкладка «Dynamic» (группа «Райсы») и строка «· Dynamic» у каждого райса во вкладке «Райсы».

Вкладка — для активного райса: облик (вариант, в форме которого стоит dynamic: Retro в цветах обоев остаётся Retro, как
в Vitreus), цвета, движок, светлая / тёмная, Wallhaven, добавить обои и сетка обоев райса с превью (⏎ — поставить,
тема перекрасится сама: хук в плагине background). Внизу — остальные райсы.

Всё делает omarchy-rice-dynamic (dotfiles: omarchy-themes/scripts); нет его в PATH — строк нет.
"""
import json
import os

from . import fsutil, paths, state
from .i18n import t

TOOL = "omarchy-rice-dynamic"
NL = "\\n"

# режимы и их описания (порядок — как в списке выбора)
SCHEMES = [
    ("vitreus", "Exactly as Vitreus: its eleven colours from the wallpaper as they are (always dark, on glass); terminal and code in shades of the accent"),
    ("wallpaper", "The wallpaper's colours read the Vitreus way, plus code and terminal colours found on the picture"),
    ("soft", "The same, quieter: the accent and the terminal colours muted"),
    ("vivid", "The same, brighter: a saturated accent and livelier terminal colours"),
    ("pure", "Only the wallpaper's colours: like “wallpaper”, but terminal and code use only hues that are really on the picture; missing ones are lighter / darker steps of them. Red stays for errors"),
    ("pure-soft", "Only the wallpaper's colours, quieter"),
    ("pure-vivid", "Only the wallpaper's colours, brighter"),
    ("mono", "Monochrome in the wallpaper's tone: everything is one hue of the picture, in different lightness; red stays for errors"),
    ("grey", "Grey, like Vitreus with the wallpaper colours off: neutral greys and red for errors; the wallpaper does not matter"),
    ("accent", "The palette of the look's variant as is; only the accent comes from the wallpaper"),
]
ALIASES = {"tonal-spot": "wallpaper", "content": "wallpaper", "fidelity": "wallpaper", "neutral": "soft",
           "vibrant": "vivid", "expressive": "vivid", "fruit-salad": "vivid", "rainbow": "vivid",
           "monochrome": "grey", "mono-tint": "mono"}
ENGINE_NOTE = ("rice — the wallpaper colours go into the rice's own palette and its generator builds every app theme in the "
               "rice's character; colors — only colors.toml, the rest comes from Omarchy templates. ⏎ switches.")


PLAIN = "plain"  # «райс без райса»: тема dynamic из любых обоев (omarchy-rice-dynamic build plain)


def theme_of(rid) -> str:
    return "dynamic" if rid == PLAIN else f"dynamic-{rid}"


def available() -> bool:
    return fsutil.which(TOOL)


def info() -> dict:
    """{райс: {engine, scheme, mode, base, look, engines, theme}} — из omarchy-rice-dynamic list --json --fast."""
    try:
        return json.loads(fsutil.run([TOOL, "list", "--json", "--fast"]) or "{}")
    except ValueError:
        return {}


def marker(rice) -> dict:
    try:
        return json.loads((paths.CONFIG / "themes" / theme_of(rice) / ".omarchy-wallpaper-theme").read_text())
    except (OSError, ValueError):
        return {}


def _preset_theme(stem) -> str:
    try:
        return str(json.loads((state.PRESET_DIR / f"{stem}.json").read_text()).get("theme") or "")
    except (OSError, ValueError):
        return ""


def base_preset(r) -> str:
    """Облик по умолчанию: dynamic.preset из rices.json, вариант с темой dynamic-<райс>, иначе первый."""
    if r.get("dynamic"):
        return r["dynamic"]
    for v in r["variants"]:
        if _preset_theme(v["preset"]) == f"dynamic-{r['id']}":
            return v["preset"]
    return r["variants"][0]["preset"] if r["variants"] else ""


def look_of(r, cfg) -> str:
    look = cfg.get("look") or ""
    return look if any(v["preset"] == look for v in r["variants"]) else base_preset(r)


def _variant_name(r, stem):
    return next((v["name"] for v in r["variants"] if v["preset"] == stem), stem)


def _rice(rid):
    return next((r for r in state.rices() if r["id"] == rid), None)


def _scheme(cfg):
    s = cfg.get("scheme") or "wallpaper"
    return ALIASES.get(s, s)


def _engine(cfg):
    e = cfg.get("engine") or "colors"
    return {"material": "colors"}.get(e, e)


# ── плитки вкладки: у строк настроек своя картинка вместо заглушки (вкладка — сетка с превью) ──

TILES = paths.CACHE / "omarchy-customizer/dynamic"


def _theme_colors(rid) -> dict:
    """colors.toml темы dynamic-<райс>: ключ → "#rrggbb"."""
    out = {}
    try:
        for line in (paths.CONFIG / "themes" / f"dynamic-{rid}" / "colors.toml").read_text().splitlines():
            k, _, v = line.partition("=")
            v = v.strip().strip('"')
            if v.startswith("#") and len(v) == 7:
                out[k.strip()] = v
    except OSError:
        pass
    return out


def _tiles(rid, wall, walls) -> dict:
    """{вид: путь к png}. Кэш по mtime colors.toml и обоям; нет Pillow или темы — пусто (останутся заглушки)."""
    c = _theme_colors(rid)
    if not c:
        return {}
    try:
        from PIL import Image, ImageDraw
    except ImportError:
        return {}
    import hashlib
    try:
        stamp = os.path.getmtime(paths.CONFIG / "themes" / f"dynamic-{rid}" / "colors.toml")
    except OSError:
        stamp = 0
    key = hashlib.md5(f"{rid}\t{stamp}\t{wall}\t{len(walls)}".encode()).hexdigest()[:12]
    W, H = 480, 300
    names = ("on", "look", "colours", "engine", "mode", "wallhaven", "add")
    paths_ = {n: TILES / f"{rid}-{n}-{key}.png" for n in names}
    if all(p.is_file() for p in paths_.values()):
        return {n: str(p) for n, p in paths_.items()}
    os.makedirs(TILES, exist_ok=True)
    for old in TILES.glob(f"{rid}-*.png"):  # прежние плитки этого райса (каталог — наш кэш)
        old.unlink(missing_ok=True)
    hexrgb = lambda h: tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))  # noqa: E731
    g = lambda k, d="#808080": hexrgb(c.get(k, d))  # noqa: E731

    def thumb(f, size=(W, H)):
        try:
            im = Image.open(f)
            im.draft("RGB", (size[0] * 2, size[1] * 2))
            im = im.convert("RGB")
            # заполнить кадр с обрезкой (как обои на экране)
            r = max(size[0] / im.width, size[1] / im.height)
            im = im.resize((max(1, int(im.width * r)), max(1, int(im.height * r))))
            x, y = (im.width - size[0]) // 2, (im.height - size[1]) // 2
            return im.crop((x, y, x + size[0], y + size[1]))
        except OSError:
            return Image.new("RGB", size, g("background"))

    base = thumb(wall) if wall else Image.new("RGB", (W, H), g("background"))
    base.save(paths_["on"])
    # облик: обои, полоса бара слева и окно в цветах темы
    im = base.copy()
    d = ImageDraw.Draw(im, "RGBA")
    d.rectangle([0, 0, 34, H], fill=g("background") + (235,))
    for i in range(4):
        d.ellipse([12, 30 + i * 22, 22, 40 + i * 22], fill=g("foreground") if i else g("accent"))
    d.rounded_rectangle([60, 40, W - 40, H - 40], 14, fill=g("background") + (225,), outline=g("accent"), width=2)
    d.rounded_rectangle([60, 40, W - 40, 72], 14, fill=g("lighter_background") + (240,))
    for i, k in enumerate(("red", "yellow", "green")):
        d.ellipse([76 + i * 18, 50, 88 + i * 18, 62], fill=g(k))
    for j, (k, w) in enumerate((("foreground", 260), ("accent", 180), ("dark_foreground", 300), ("blue", 140),
                                 ("foreground", 220))):
        d.rounded_rectangle([84, 92 + j * 26, 84 + w, 104 + j * 26], 5, fill=g(k))
    im.save(paths_["look"])
    # цвета: полосы палитры
    im = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(im)
    keys = ["darker_background", "background", "lighter_background", "selection", "dark_foreground", "foreground",
            "accent", "red", "green", "yellow", "blue", "magenta", "cyan"]
    bw = W / len(keys)
    for i, k in enumerate(keys):
        d.rectangle([int(i * bw), 0, int((i + 1) * bw), H], fill=g(k))
    im.save(paths_["colours"])
    # движок: 16 цветов терминала сеткой на фоне
    im = Image.new("RGB", (W, H), g("background"))
    d = ImageDraw.Draw(im)
    ansi = ["red", "green", "yellow", "blue", "magenta", "cyan", "foreground", "accent"]
    for r_, pre in enumerate(("", "bright_")):
        for i, k in enumerate(ansi):
            col = c.get(pre + k) or c.get(k) or "#808080"
            d.rounded_rectangle([24 + i * 56, 70 + r_ * 90, 70 + i * 56, 146 + r_ * 90], 8, fill=hexrgb(col))
    im.save(paths_["engine"])
    # светлая / тёмная: фон темы и текст на нём
    im = Image.new("RGB", (W, H), g("background"))
    d = ImageDraw.Draw(im)
    for j, k in enumerate(("foreground", "dark_foreground", "accent", "foreground", "dark_foreground")):
        d.rounded_rectangle([40, 50 + j * 42, 40 + (380 - j * 40), 66 + j * 42], 6, fill=g(k))
    im.save(paths_["mode"])
    # Wallhaven и «добавить»: мозаика из обоев пула
    for n, pick in (("wallhaven", walls[-4:]), ("add", walls[:4])):
        im = Image.new("RGB", (W, H), g("background"))
        for i, f in enumerate(pick[:4]):
            im.paste(thumb(f, (W // 2 - 6, H // 2 - 6)), ((i % 2) * (W // 2) + 3, (i // 2) * (H // 2) + 3))
        d = ImageDraw.Draw(im, "RGBA")
        d.rounded_rectangle([W // 2 - 44, H // 2 - 44, W // 2 + 44, H // 2 + 44], 22, fill=g("background") + (225,))
        if n == "add":
            d.rectangle([W // 2 - 26, H // 2 - 5, W // 2 + 26, H // 2 + 5], fill=g("accent"))
            d.rectangle([W // 2 - 5, H // 2 - 26, W // 2 + 5, H // 2 + 26], fill=g("accent"))
        else:
            d.ellipse([W // 2 - 26, H // 2 - 26, W // 2 + 12, H // 2 + 12], outline=g("accent"), width=8)
            d.line([W // 2 + 6, H // 2 + 6, W // 2 + 28, H // 2 + 28], fill=g("accent"), width=10)
        im.save(paths_[n])
    return {n: str(p) for n, p in paths_.items()}


# ── dynamic без райса: строки для вкладки «Тема» и раздела во вкладке Dynamic ──

def plain_rows(cfg=None) -> list:
    if not available():
        return []
    cfg = cfg if cfg is not None else info().get(PLAIN, {})
    on = state.theme_name() == "dynamic"
    scheme, mode = _scheme(cfg), cfg.get("mode") or "auto"
    src = os.path.basename(marker(PLAIN).get("image", "")) or t("current wallpaper")
    out = [f"{t('🎨 Dynamic — theme from the wallpaper')}\tdynamic:{PLAIN}\t\t{'1' if on else '0'}\t"
           + t("The “dynamic” theme from any wallpaper (%s), no rice: colours by the chosen mode, and it recolours itself when the wallpaper changes.", src)]
    out.append(f"{t('🎨 Dynamic › colours: %s', scheme)}\tdynamic-scheme:{PLAIN}\t\t0\t"
               + t(dict(SCHEMES).get(scheme, scheme)) + NL + NL + t("Pick how the colours are read from the wallpaper."))
    out.append(f"{t('🎨 Dynamic › light / dark: %s', mode)}\tdynamic-mode:{PLAIN}\t\t0\t"
               + t("auto — by the wallpaper: a light picture gives a light theme; dark or light — always so.")
               + NL + NL + t("In the accent mode the palette is the theme that was on before dynamic, the accent from the wallpaper."))
    return out


# ── вкладка «Райсы»: одна строка на райс ──

def rows(r, cfg) -> list:
    rid, name = r["id"], r["name"]
    theme = f"dynamic-{rid}"
    if any(_preset_theme(v["preset"]) == theme for v in r["variants"]):
        return []  # вариант райса уже и есть dynamic (Vitreus · Стекло)
    on = state.theme_name() == theme
    src = os.path.basename(marker(rid).get("image", "")) or t("current wallpaper")
    return [f"{name} · Dynamic\tdynamic:{rid}\t\t{'1' if on else '0'}\t"
            + t("The look of %s with colours from the wallpaper (%s).", name, src) + NL + NL
            + t("Settings, the rice's wallpapers and Wallhaven are on the Dynamic tab.")]


# ── вкладка «Dynamic» ──

def tab() -> list:
    if not available():
        return [f"{t('omarchy-rice-dynamic is not on PATH')}\tsection:none\t\t0\t\theader"]
    dyn = info()
    rices = [r for r in state.rices() if r["id"] in dyn]
    if not rices:
        return []
    cur = state.current_rice()
    on_theme = state.theme_name()
    r = next((x for x in rices if on_theme == f"dynamic-{x['id']}"), None) \
        or next((x for x in rices if x["id"] == cur), None) or rices[0]
    rid, name, cfg = r["id"], r["name"], dyn[r["id"]]
    theme = f"dynamic-{rid}"
    on = on_theme == theme
    look = look_of(r, cfg)
    scheme, engine = _scheme(cfg), _engine(cfg)
    mode = cfg.get("mode") or "auto"
    src = os.path.basename(marker(rid).get("image", "")) or t("current wallpaper")
    walls = [w for w in fsutil.run([TOOL, "list", rid]).split("\n") if w]
    wall = marker(rid).get("image") or (walls[0] if walls else "")
    tl = _tiles(rid, wall if wall and os.path.isfile(wall) else "", walls)
    out = [f"{name} · Dynamic\tsection:{name}\t\t0\t\theader"]
    out.append(f"{t('Dynamic is on') if on else t('Turn Dynamic on')}\tdynamic:{rid}\t{tl.get('on', '')}\t{'1' if on else '0'}\t"
               + t("The look of %s with colours from the wallpaper (%s).", name, src) + NL + NL
               + t("Colours are taken from the wallpaper and follow it: pick another wallpaper of the rice and the theme recolours itself. Theme: %s.", theme))
    if len(r["variants"]) > 1:  # облик выбирать есть из чего
        out.append(f"{t('look: %s', _variant_name(r, look))}\tdynamic-look:{rid}\t{tl.get('look', '')}\t0\t"
                   + t("The variant whose form the theme wears: its style, bar, fonts and corners, in the wallpaper's colours. Retro with the wallpaper's colours is still Retro, as in Vitreus."))
    note = t(dict(SCHEMES).get(scheme, scheme))
    if scheme == "accent" and engine != "rice":
        note += NL + NL + t("With the colors engine the palette is the look's colors.toml as is, the accent from the wallpaper; dark / light turns it over.")
    if scheme == "vitreus" and engine != "rice":
        note += NL + NL + t("Only the rice engine keeps the exact palette; colors works like “wallpaper”.")
    out.append(f"{t('colours: %s', scheme)}\tdynamic-scheme:{rid}\t{tl.get('colours', '')}\t0\t" + note + NL + NL
               + t("Pick how the colours are read from the wallpaper."))
    if len(cfg.get("engines") or []) > 1:
        out.append(f"{t('engine: %s', engine)}\tdynamic-engine:{rid}\t{tl.get('engine', '')}\t0\t" + t(ENGINE_NOTE))
    out.append(f"{t('light / dark: %s', mode)}\tdynamic-mode:{rid}\t{tl.get('mode', '')}\t0\t"
               + t("auto — by the wallpaper: a light picture gives a light theme (a rice may keep its own: Vitreus Glass is always dark); dark or light — always so.")
               + NL + NL + t("In the accent mode: auto — as the look's variant; dark or light — the variant's palette turned to that mode (Retro dark: the same hues, backgrounds and ink swapped in lightness)."))
    out.append(f"{t('find wallpapers on Wallhaven…')}\tdynamic-wallhaven:{rid}\t{tl.get('wallhaven', '')}\t0\t"
               + t("Search wallhaven.cc (safe for work only), pick pictures in the wallpaper picker one by one: each is downloaded into the rice's wallpapers (%s, not in git). Esc — done.",
                   paths.tilde(paths.CONFIG / "backgrounds" / theme)))
    out.append(f"{t('add wallpapers…')}\tdynamic-add:{rid}\t{tl.get('add', '')}\t0\t"
               + t("Add images or live wallpapers to the rice: locally (%s, not in git) or into the repo (omarchy-themes/<rice>/wallpapers).",
                   paths.tilde(paths.CONFIG / "backgrounds" / theme)))
    # сетка обоев райса: превью — сама картинка, ⏎ — поставить (и перекрасить)
    from .lists_more import _wall_row
    out.append(f"{t('Wallpapers of %s (%s)', name, len(walls))}\tsection:walls\t\t0\t\theader")
    cur_bg = state.current_bg()
    for w in walls:
        row = _wall_row(w, cur_bg).split("\t")
        row[1] = "dynamic-wall:" + rid + ":" + w
        parts = w.split("/")
        if len(parts) > 2 and parts[-2] == "backgrounds" and "omarchy-themes" in parts:
            row[0] = f"{parts[-3]} · {row[0]}"  # 1-liquid.png есть у каждого варианта — подписать вариантом
        out.append("\t".join(row))
    plain = plain_rows(dyn.get(PLAIN, {}))
    if plain:
        out.append(f"{t('No rice')}\tsection:plain\t\t0\t\theader")
        out += plain
    others = [x for x in rices if x["id"] != rid]
    if others:
        out.append(f"{t('Other rices')}\tsection:others\t\t0\t\theader")
        for x in others:
            out.append(f"{x['name']} · Dynamic\tdynamic:{x['id']}\t\t0\t"
                       + t("The look of %s with colours from the wallpaper (%s).", x["name"],
                           os.path.basename(marker(x["id"]).get("image", "")) or t("current wallpaper")))
    return out


def _set(rid, *opts):
    """Запомнить настройку; если тема райса сейчас текущая — пересобрать и применить."""
    from .apply_ops import notify, sh
    applied = state.theme_name() == theme_of(rid)
    if applied:
        notify("-t", "3000", "Dynamic", t("Recolouring from the wallpaper…"))
    code, out = sh([TOOL, "set", rid, *opts, *([] if applied else ["--no-apply"])], quiet=False)
    if code != 0:
        notify("-u", "critical", "Dynamic", t("Could not build the theme"))
    elif applied:
        notify("-t", "3000", "Dynamic", out.strip().split("\n")[-1])


def apply(value):
    from .apply_ops import Exit, _pick_images, _zenity, apply_preset, notify, sh
    kind, rest = value.split(":", 1)
    if kind == "section":
        return
    rid, _, arg = rest.partition(":")
    if rid == PLAIN:
        if kind == "dynamic":
            notify("-t", "3000", "Dynamic", t("Building a theme from the wallpaper…"))
            code, out = sh([TOOL, "build", PLAIN], quiet=False)
            notify(*(["-t", "3000", "Dynamic", out.strip().split("\n")[-1]] if code == 0
                     else ["-u", "critical", "Dynamic", t("Could not build the theme")]))
            return
        if kind not in ("dynamic-scheme", "dynamic-mode"):
            raise Exit(1)
        r = {"id": PLAIN, "name": "Dynamic", "variants": []}
    else:
        r = _rice(rid)
    if not r:
        raise Exit(1)
    cfg = info().get(rid, {})
    theme = f"dynamic-{rid}"
    if kind == "dynamic":
        notify("-t", "3000", "Dynamic", t("Building a theme from the wallpaper…"))
        if sh([TOOL, "build", rid, "--no-apply"])[0] != 0:
            notify("-u", "critical", "Dynamic", t("Could not build the theme"))
            raise Exit(1)
        apply_preset(str(state.PRESET_DIR / f"{look_of(r, cfg)}.json"), theme=theme, wallpaper=marker(rid).get("image"))
    elif kind == "dynamic-look":
        rows_ = [x for v in r["variants"] for x in (v["preset"], v["name"])]
        pick = _zenity(["--list", f"--title={t('Look of %s', r['name'])}", "--width=420", "--height=420",
                        "--print-column=1", "--hide-column=1", "--column=id", f"--column={t('Variant')}", *rows_])
        if not pick:
            raise Exit(0)
        stem = pick.split("|")[0]
        sh([TOOL, "set", rid, "--look", stem, "--no-apply"])
        if state.theme_name() == theme or state.current_rice() == rid:
            apply(f"dynamic:{rid}")  # облик меняется только применением пресета
    elif kind == "dynamic-scheme":
        rows_ = [x for s, d in SCHEMES for x in (s, t(d))]
        pick = _zenity(["--list", f"--title={t('Colours from the wallpaper')}", "--width=720", "--height=560",
                        f"--column={t('Mode')}", f"--column={t('What it does')}", *rows_])
        if pick:
            _set(rid, "--scheme", pick.split("|")[0])
    elif kind == "dynamic-engine":
        _set(rid, "--engine", "colors" if _engine(cfg) == "rice" else "rice")
    elif kind == "dynamic-mode":
        pick = _zenity(["--list", f"--title={t('Light / dark')}", "--width=360", "--height=260",
                        f"--column={t('Mode')}", "auto", "dark", "light"])
        if pick:
            _set(rid, "--mode", pick.split("|")[0])
    elif kind == "dynamic-wall":
        if not os.path.isfile(arg):
            raise Exit(1)
        if state.theme_name() != theme:
            # сначала облик в dynamic — на этих обоях (хук потом ничего не делает: тема уже из них)
            if sh([TOOL, "build", rid, arg, "--no-apply"])[0] != 0:
                notify("-u", "critical", "Dynamic", t("Could not build the theme"))
                raise Exit(1)
            apply_preset(str(state.PRESET_DIR / f"{look_of(r, cfg)}.json"), theme=theme, wallpaper=arg)
        else:
            sh(["omarchy", "theme", "bg", "set", arg])  # хук плагина обоев перекрасит тему
    elif kind == "dynamic-wallhaven":
        query = _zenity(["--entry", f"--title={t('Wallhaven')}", "--width=480",
                         f"--text={t('Search wallhaven.cc for %s (safe for work only):', r['name'])}",
                         f"--entry-text={r.get('wallhaven') or 'abstract'}"])
        if not query:
            raise Exit(0)
        notify("-t", "3000", "Wallhaven", t("Searching “%s”…", query))
        code, out = sh([TOOL, "wallhaven", "search", rid, query], quiet=False)
        thumbs = out.strip().split("\n")[-1] if code == 0 else ""
        if not thumbs or not os.path.isdir(thumbs):
            notify("-u", "critical", "Wallhaven", t("Could not reach Wallhaven"))
            raise Exit(1)
        got = 0
        while True:  # по одной: выбранная качается в пул, пикер открывается снова; Esc — хватит
            pick = fsutil.run(["omarchy-menu-images", thumbs]).strip()
            if not pick:
                break
            notify("-t", "2000", "Wallhaven", t("Downloading…"))
            if sh([TOOL, "wallhaven", "get", rid, pick, "--local"])[0] == 0:
                got += 1
                os.remove(pick)  # из выбора — уже в пуле (файл кэша поиска)
            else:
                notify("-u", "critical", "Wallhaven", t("Could not download it"))
        if got:
            notify("-t", "3000", "Wallhaven", t("Added %s wallpaper(s) to %s", got, r["name"]))
    elif kind == "dynamic-add":
        files = [f for f in _pick_images(t("Wallpapers for %s", r["name"])) if f]
        if not files:
            raise Exit(0)
        where = _zenity(["--list", f"--title={t('Add wallpapers')}", "--width=640", "--height=260",
                         f"--text={t('Where to keep them?')}", f"--column={t('Where')}", f"--column={t('What it means')}",
                         "--print-column=1", "local", t("Only on this machine, not in git"),
                         "repo", t("omarchy-themes/%s/wallpapers — mind the licence of the pictures: the repo is public", rid)])
        if not where:
            raise Exit(0)
        code, _ = sh([TOOL, "add", rid, *files, "--repo" if where.split("|")[0] == "repo" else "--local"], quiet=False)
        notify("-t", "3000", "Dynamic", t("Added %s wallpaper(s) to %s", len(files), r["name"]) if code == 0 else t("Could not add the wallpapers"))
