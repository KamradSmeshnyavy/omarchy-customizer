#!/usr/bin/env python3
# Генератор встроенных стилей styles/*.json: одна таблица на все стили, проверка полноты (у каждого стиля —
# те же ручки, что у DOT-MATRIX) перед записью. DOT-MATRIX собирается из пресета-источника (свой пресет в духе Nothing).
#
#   python3 scripts/gen-styles.py <каталог плагина> <пресет-источник DOT-MATRIX.json>
#   python3 scripts/check-styles.py            # только проверить
import json, os, sys

plugin = sys.argv[1]
src = sys.argv[2]  # nothing-hacking.json
out = os.path.join(plugin, "styles")

# «Содержимое», а не форма: что видно и в каком формате — остаётся за пользователем.
CONTENT = {
    "widgets": ["clock", "visualizer", "sysinfo", "edgeHover", "dashMedia", "dashCalendar", "dashWeather", "dashStats"],
    "lock": ["clock24", "showSeconds", "showDate"],
    "sounds": ["sounds", "soundVolume"],
    "imagePicker": ["autoCache"],
    "glyph": ["glyphCharger", "glyphCriticalRed"],
    "osd": ["osdShowValue"],
}

nh = json.load(open(src))
dotmatrix = {k: v for k, v in nh.items() if k not in ("theme", "wallpaper", "name", "name_ru", "note", "note_ru")}
for sec, keys in CONTENT.items():
    for k in keys:
        dotmatrix.get(sec, {}).pop(k, None)
dotmatrix["hyprGeometry"]["noGaps"] = True
dotmatrix["notifications"].setdefault("notifyAttach", "auto")
dotmatrix["fonts"] = "pixel"
# Как рабочий стол NIHIL: часы, сеть и плеер одной колонкой карточек в левом верхнем углу.
dotmatrix["widgets"].update(settingsPanel="drawer", powerStyle="edge", clipboardPanel="stock")
dotmatrix["widgets"].update(network=True, networkAnchor="top-left", media=True, mediaAnchor="top-left", home=False, deck=False,
                           homeLayout="glyph", homeCards="glyph", homeHideWidgets=True, deckLayout="panel", deckCards="glyph",
                           deckTrigger="dwell")
# Nothing: плоское «железо» — без теней, сплошные поверхности, шрифт профиля.
dotmatrix["look"] = {"elevation": 0, "motion": 1, "material": "solid", "cornerScale": 1, "typeface": "profile", "texture": ""}
dotmatrix = {
    "name": "DOT-MATRIX", "name_ru": "DOT-MATRIX",
    "note": "Nothing-inspired hardware shell on any theme: bezel frame with windows flush against it, vertical LED bar, dot-matrix typography, signal colour strictly for alerts, perimeter Glyph lighting, LED dashboard/OSD/launcher/lock and a tactile sound pack.",
    "note_ru": "Аппаратная оболочка в духе Nothing на любой теме: рамка-бортик с окнами вплотную, вертикальный LED-бар, матричная типографика, сигнальный цвет строго для тревог, контурная подсветка Glyph, LED-дашборд/OSD/лаунчер/локскрин и тактильный звуковой пакет.",
    **dotmatrix,
}


# Glyph (по мотивам glyph-rice): та же «аппаратная» основа, что у DOT-MATRIX, но без рамки-бортика — узкая
# плавающая пилюля слева (RunCat, таймер фокуса), домашний экран glyph и Deck снизу, OSD подсветкой по краю,
# пикер обоев «точки», шрифты nothing (точки только в часах и цифрах), красный строго для тревог.
import copy
glyph = copy.deepcopy(dotmatrix)
glyph.update({
    "name": "Glyph", "name_ru": "Glyph",
    "note": "After glyph-rice: Nothing OS on a floating left pill — dot-matrix clocks and numbers, a home screen with a bento of round and square tiles on an empty workspace, a deck from the bottom edge, edge-light OSD and perimeter Glyph lighting, signal red only for alerts.",
    "note_ru": "По мотивам glyph-rice: Nothing OS на плавающей пилюле слева — точечные часы и цифры, домашний экран с бенто из круглых и квадратных плиток на пустом столе, Deck из-под нижнего края, OSD подсветкой по краю и контурная подсветка Glyph, красный только для тревог.",
    "fonts": "nothing",
})
glyph.pop("barSkinData", None)
glyph.pop("barLayoutData", None)
glyph.update({"barSkin": "glyph-pill", "barLayout": "glyph-rice"})
glyph["hyprGeometry"] = {"gapsIn": 6, "gapsOut": 12, "borderSize": 1, "rounding": 18, "shadow": False, "noGaps": False}
glyph["imagePicker"] = dict(glyph["imagePicker"], style="glyph", cardRadius=24)
# переключатель обоев, лок и переход — из glyph-rice
glyph["lock"] = dict(glyph["lock"], design="glyph", wallpaperBlur=0, wallpaperDim=0.35)
glyph["launcher"] = dict(glyph["launcher"], skin="glyph", backdrop=0.74)
glyph["wallpaperFx"] = dict(glyph["wallpaperFx"], type="dotwave", duration=1500, easing="InOutSine")
glyph["widgets"].update(settingsPanel="quick", powerStyle="glyph", clipboardPanel="glyph", home=True, homeLayout="glyph", homeCards="glyph", homeHideWidgets=True,
                        deck=True, deckLayout="panel", deckCards="glyph", deckTrigger="dwell",
                        dashAttach="floating", dashAnimation="grow")
glyph["osd"].update(osdStyle="edge", osdAttach="floating")
glyph["look"] = dict(glyph["look"], cornerScale=1.4)


def plain(name, name_ru, note, note_ru, *, geom, bar, opacity, blur, anims, lock, launcher, radius, alpha,
          cards, fx, picker, dash_anim, sound_pack, window_sounds, fonts, look, osd_side="right", attach="auto", shader="off"):
    return {
        "name": name, "name_ru": name_ru, "note": note, "note_ru": note_ru,
        "anims": anims, "opacity": opacity, "blur": blur, "shader": shader,
        "hyprGeometry": {**geom, "noGaps": False},
        "barSkin": bar, "barLayout": "omarchy-stock", "barTransparent": False,
        "lock": {"design": lock, "wallpaperBlur": 0.6 if lock == "style-glass" else 0, "wallpaperDim": 0.35},
        "launcher": {"skin": launcher, "backdrop": 0.6 if alpha < 0.9 else 0.75},
        "wallpaperFx": fx,
        "imagePicker": {"style": picker, "cardRadius": radius, "selectedBorder": 2 if cards == "flat" else 1, "dim": 0.5},
        "widgets": {
            "widgetStyle": "style", "clockStyle": "big" if cards != "flat" else "minimal",
            "network": False, "networkAnchor": "top-left", "media": True, "mediaAnchor": "bottom-left",
            "dashStyle": "default", "dashFollowBar": True, "dashAttach": attach, "dashBackground": "background",
            "dashAlpha": alpha, "dashRadius": radius, "dashBorder": cards != "flat",
            "dashAnimation": dash_anim, "dashDuration": fx["duration"] // 2 + 100,
            # Домашний экран и Deck — свои у стиля Glyph; остальные их выключают, чтобы не оставались после него.
            "home": False, "deck": False, "homeLayout": "glyph", "homeCards": "style", "homeHideWidgets": True,
            "deckLayout": "panel", "deckCards": "style", "deckTrigger": "dwell", "settingsPanel": "drawer",
            "powerStyle": "edge", "clipboardPanel": "stock",
            # терминал на обоях — свой у Retro CRT (его term-виджет), остальные стили его убирают
            "term": False, "termAnchor": "top-left",
        },
        "osd": {
            "osdStyle": "edge", "osdFollowBar": True, "osdAttach": attach, "osdBackground": "background",
            "osdAlpha": alpha, "osdRadius": radius, "osdSide": osd_side, "osdAlign": "center",
        },
        "notifications": {
            "notifyStyle": "drawer", "notifyFollowBar": True, "notifyAttach": attach, "notifyBackground": "background", "notifyAlpha": alpha,
            "notifyRadius": radius, "notifyCards": cards, "notifyCorner": "top-right", "notifyWidth": 380,
        },
        "sounds": {"soundPack": sound_pack, "windowSounds": window_sounds},
        "glyph": {"glyphEnabled": False, "glyphColor": "foreground", "glyphCriticalColor": "urgent",
                  "glyphDuration": 1100, "glyphThickness": 2.5, "glyphInsetMode": "auto"},
        "fonts": fonts,
        "look": {"texture": "", **look},
    }


styles = {
    "dotmatrix": dotmatrix,
    "glyph": glyph,
    "flat": plain(
        "Flat", "Плоский",
        "Flat / Metro: square corners, solid surfaces, no shadows or blur, quick motion, quiet. Typography and colour do all the work.",
        "Flat / Metro: прямые углы, сплошные поверхности, без теней и блюра, быстрые анимации, тихо. Всю работу делают шрифт и цвет.",
        geom={"gapsIn": 4, "gapsOut": 8, "borderSize": 2, "rounding": 0, "shadow": False},
        bar="solid-accent", opacity="solid", blur="off", anims="ML4W - fast", lock="style-flat", launcher="drawer-flat",
        radius=0, alpha=1, cards="flat", fx={"type": "fade", "duration": 300, "easing": "OutCubic"},
        picker="slices", dash_anim="fade", sound_pack="flat", window_sounds=True, fonts="stock",
        look={"elevation": 0, "motion": 0.7, "material": "solid", "cornerScale": 0, "typeface": "shell"}),
    "glass": plain(
        "Glass", "Стекло",
        "Glassmorphism: translucent windows over a frosted wallpaper, glass bar and panels, soft round corners, smooth motion and soft clicks.",
        "Глассморфизм: полупрозрачные окна над матовыми обоями, стеклянный бар и панели, мягкие скругления, плавные анимации и мягкие щелчки.",
        geom={"gapsIn": 6, "gapsOut": 14, "borderSize": 1, "rounding": 16, "shadow": True},
        bar="glass", opacity="frosted", blur="frosted", anims="HYDE - default", lock="style-glass", launcher="drawer-glass",
        radius=18, alpha=0.75, cards="bordered", fx={"type": "fade", "duration": 700, "easing": "OutCubic"},
        picker="cards", dash_anim="grow", sound_pack="glass", window_sounds=True, fonts="stock",
        look={"elevation": 1, "motion": 1.25, "material": "glass", "cornerScale": 1.2, "typeface": "shell"}),
    "liquid": plain(
        "Liquid Glass", "Жидкое стекло",
        "Liquid glass (after Vitreus): very clear panels under strong vivid blur with a light rim and a soft top highlight, a floating glass pill bar, big soft corners; the dashboard flows out of the bar like a drop and springs into place.",
        "Жидкое стекло (по мотивам Vitreus): очень прозрачные панели под сильным сочным блюром со светлым ободком и мягким бликом сверху, плавающая стеклянная пилюля-бар, крупные мягкие скругления; дашборд вытекает из бара каплей и пружинит на место.",
        geom={"gapsIn": 8, "gapsOut": 16, "borderSize": 1, "rounding": 22, "shadow": True},
        bar="liquid", opacity="frosted", blur="liquid", anims="HYDE - default", lock="liquid", launcher="liquid",
        radius=22, alpha=0.42, cards="bordered", fx={"type": "hexreveal", "duration": 900, "easing": "OutCubic"},
        picker="honeycomb", dash_anim="liquid", sound_pack="glass", window_sounds=True, fonts="vitreus-glass",
        look={"elevation": 1, "motion": 1.2, "material": "liquid", "cornerScale": 1.3, "typeface": "shell"}),
    "fluent": plain(
        "Fluent", "Fluent",
        "Material / Fluent: layered surfaces with depth — gentle rounding, real shadows, a hint of translucency, island bar, card panels and the theme's own sounds.",
        "Material / Fluent: слои с глубиной — умеренные скругления, настоящие тени, лёгкая полупрозрачность, бар-острова, карточки и звуки самой темы.",
        geom={"gapsIn": 5, "gapsOut": 10, "borderSize": 1, "rounding": 8, "shadow": True},
        bar="islands", opacity="soft", blur="medium", anims="01-default - v2", lock="style-fluent", launcher="drawer-fluent",
        radius=10, alpha=0.9, cards="bordered", fx={"type": "fade", "duration": 450, "easing": "OutCubic"},
        picker="cards", dash_anim="slide", sound_pack="fluent", window_sounds=True, fonts="nothing",
        look={"elevation": 2, "motion": 1, "material": "auto", "cornerScale": 0.8, "typeface": "profile"}),    "neumorph": plain(
        "Neumorphism", "Неоморфизм",
        "Neumorphism: soft extruded plastic — no borders, panels in the background colour with a light and a dark shadow, generous round corners, muted soft sounds.",
        "Неоморфизм: мягкий выдавленный пластик — без рамок, панели цвета фона со светлой и тёмной тенью, крупные скругления, приглушённые мягкие звуки.",
        geom={"gapsIn": 10, "gapsOut": 22, "borderSize": 0, "rounding": 18, "shadow": True},
        bar="soft", opacity="solid", blur="off", anims="HYDE - minimal-1", lock="style-neumorph", launcher="drawer-neumorph",
        radius=20, alpha=1, cards="flat", fx={"type": "fade", "duration": 550, "easing": "OutCubic"},
        picker="cards", dash_anim="grow", sound_pack="neumorph", window_sounds=True, fonts="nothing",
        attach="floating",
        look={"elevation": 1, "motion": 1.0, "material": "soft", "cornerScale": 1.3, "typeface": "profile"}),
    "brutal": plain(
        "Brutalism", "Брутализм",
        "Brutalism: square everything, thick ink borders, hard offset shadows without blur, no transparency, fast motion and hard clicks.",
        "Брутализм: всё прямоугольное, толстые рамки цвета текста, жёсткие смещённые тени без размытия, никакой прозрачности, быстрые анимации и жёсткие клики.",
        geom={"gapsIn": 8, "gapsOut": 16, "borderSize": 3, "rounding": 0, "shadow": False},
        bar="brutal", opacity="solid", blur="off", anims="ML4W - fast", lock="style-brutal", launcher="drawer-brutal",
        radius=0, alpha=1, cards="bordered", fx={"type": "fade", "duration": 250, "easing": "OutCubic"},
        picker="slices", dash_anim="fade", sound_pack="brutal", window_sounds=True, fonts="stock",
        attach="floating",
        look={"elevation": 0, "motion": 0.6, "material": "brutal", "cornerScale": 0, "typeface": "shell"}),
    "retro": plain(
        "Retro 9x", "Ретро 9x",
        "Retro desktop of the nineties: grey panels with a 3D bevel, square windows, pixel interface font, no animations and chiptune sounds.",
        "Ретро-десктоп девяностых: серые панели с объёмным кантом, квадратные окна, пиксельный шрифт интерфейса, без анимаций и чиптюн-звуки.",
        geom={"gapsIn": 3, "gapsOut": 6, "borderSize": 2, "rounding": 0, "shadow": False},
        bar="bevel", opacity="solid", blur="off", anims="03- Disable Animation", lock="style-retro", launcher="drawer-retro",
        radius=0, alpha=1, cards="bordered", fx={"type": "fade", "duration": 200, "easing": "OutCubic"},
        picker="slices", dash_anim="fade", sound_pack="retro", window_sounds=True, fonts="retro",
        attach="floating",
        look={"elevation": 0, "motion": 0, "material": "bevel", "cornerScale": 0, "typeface": "profile"}),
    "neon": plain(
        "Neon / Cyber", "Неон",
        "Neon / cyber: dark glass, borders and panels glowing in the accent colour, a light scanline shader over the screen and synth sounds with a filter sweep.",
        "Неон / кибер: тёмное стекло, рамки и панели светятся цветом акцента, лёгкий шейдер строк развёртки на экране и синт-звуки с проходом фильтра.",
        geom={"gapsIn": 6, "gapsOut": 14, "borderSize": 2, "rounding": 8, "shadow": True},
        bar="neon", opacity="glass", blur="strong", anims="END-4", lock="style-neon", launcher="drawer-neon",
        radius=10, alpha=0.9, cards="bordered", fx={"type": "fade", "duration": 500, "easing": "OutCubic"},
        picker="cards", dash_anim="slide", sound_pack="neon", window_sounds=True, fonts="stock",
        attach="floating", shader="neon",
        look={"elevation": 1, "motion": 1.1, "material": "glow", "cornerScale": 0.8, "typeface": "shell"}),
    "paper": plain(
        "Paper", "Бумага",
        "Paper / sketchbook: panels are sheets of paper with a torn bottom edge, grain and a strip of tape, handwritten Caveat, a paper bar, a paper grain shader over the whole screen and calm motion. Colours stay the theme's: a light theme gives white paper, a dark one — kraft.",
        "Бумага / скетчбук: панели — листы с рваным нижним краем, зерном и полоской скотча, рукописный Caveat, бумажный бар, шейдер бумажного зерна на весь экран и спокойные анимации. Цвета остаются от темы: светлая даёт белую бумагу, тёмная — крафт.",
        geom={"gapsIn": 8, "gapsOut": 18, "borderSize": 2, "rounding": 6, "shadow": True},
        bar="paper", opacity="solid", blur="off", anims="ML4W - standard", lock="style-paper", launcher="drawer-paper",
        radius=8, alpha=1, cards="bordered", fx={"type": "fade", "duration": 600, "easing": "OutCubic"},
        picker="cards", dash_anim="fade", sound_pack="paper", window_sounds=True, fonts="paper-ui",
        attach="floating", shader="paper",
        look={"elevation": 2, "motion": 1.1, "material": "paper", "cornerScale": 0.5, "typeface": "hand",
              "texture": "~/.config/omarchy/plugins/kamradsmeshnyavy.customizer/textures/paper.png"}),
    "yami": plain(
        "yami", "yami",
        "After yami (Trendorin/yami, MIT): a pixel-art desktop in dark graphite with one accent — square windows with a one-pixel border, a thin top bar with square workspace cells and cpu / ram scales, flat panels with a hard pixel shadow, the pixel Tiny5 font in the whole shell, quick motion.",
        "По мотивам yami (Trendorin/yami, MIT): пиксельный рабочий стол в тёмном графите с одним акцентом — квадратные окна с рамкой в пиксель, тонкий бар сверху с квадратными ячейками столов и шкалами cpu / ram, плоские панели с жёсткой пиксельной тенью, пиксельный Tiny5 во всей оболочке, быстрые анимации.",
        geom={"gapsIn": 4, "gapsOut": 8, "borderSize": 2, "rounding": 0, "shadow": False},
        bar="yami", opacity="solid", blur="off", anims="yami", lock="yami", launcher="yami",
        radius=0, alpha=1, cards="bordered", fx={"type": "fade", "duration": 260, "easing": "OutCubic"},
        picker="slices", dash_anim="fade", sound_pack="flat", window_sounds=True, fonts="yami",
        attach="floating",
        look={"elevation": 0, "motion": 0.7, "material": "pixel", "cornerScale": 0, "typeface": "hand"}),
    "rumda": plain(
        "Rumda", "Rumda",
        "After Rumda (hexonide/rumda): a warm coffee or sand desktop with a caramel accent — a narrow pill bar on the left with every module in its own card, windows with a 3 px border and corners of 7, a dense dashboard with a GitHub graph, the pixel Dogica Pixel font in the shell, windows sliding in from below.",
        "По мотивам Rumda (hexonide/rumda): тёплый кофейный или песочный стол с карамельным акцентом — узкая пилюля-бар слева, каждый модуль в своей карточке, окна с рамкой 3 px и углами 7, плотный дашборд с графиком GitHub, пиксельный Dogica Pixel в оболочке, окна въезжают снизу.",
        geom={"gapsIn": 9, "gapsOut": 40, "borderSize": 3, "rounding": 7, "shadow": True},
        bar="rumda", opacity="solid", blur="off", anims="rumda", lock="rumda", launcher="rumda",
        radius=7, alpha=1, cards="bordered", fx={"type": "fade", "duration": 400, "easing": "OutCubic"},
        picker="cards", dash_anim="fade", sound_pack="paper", window_sounds=True, fonts="rumda",
        attach="floating",
        look={"elevation": 1, "motion": 1.0, "material": "solid", "cornerScale": 0.4, "typeface": "hand"}),
    "bruteon": plain(
        "Bruteon", "Bruteon",
        "After Bruteon by Darkkal44 (neo-brutalism, look from its screenshots): warm cream paper, everything outlined in thick dark ink with a hard shadow without blur, pastel tiles — three islands of a bar, a dashboard of cards, windows with a 3 px border and a 6 × 6 hard shadow, springy pop-ins, JetBrains Mono.",
        "По мотивам Bruteon (Darkkal44, необрутализм, облик с его скриншотов): тёплая кремовая бумага, всё обведено толстым тёмным контуром с жёсткой тенью без размытия, пастельные плитки — три острова бара, дашборд из карточек, окна с рамкой 3 px и жёсткой тенью 6 × 6, упругие появления, JetBrains Mono.",
        geom={"gapsIn": 8, "gapsOut": 18, "borderSize": 3, "rounding": 10, "shadow": True},
        bar="bruteon", opacity="solid", blur="off", anims="bruteon", lock="style-brutal", launcher="drawer-brutal",
        radius=10, alpha=1, cards="bordered", fx={"type": "fade", "duration": 300, "easing": "OutCubic"},
        picker="cards", dash_anim="fade", sound_pack="brutal", window_sounds=True, fonts="cozytile",
        attach="floating",
        look={"elevation": 1, "motion": 0.8, "material": "brutal", "cornerScale": 0.8, "typeface": "shell"}),
    "cozytile": plain(
        "Cozytile", "Cozytile",
        "After Cozytile by Darkkal44 (look only): a floating 30 px pill bar with dark tabs that have S-shaped slanted sides, workspace dots, borderless windows with 9 px gaps, corners of 10 and a soft shadow, plain fades instead of animations, a 400 px launcher with a picture header, a power menu of five big icons, the Orbitron lock with falling petals, JetBrains Mono everywhere.",
        "По мотивам Cozytile (Darkkal44, только облик): плавающий бар-пилюля 30 px с тёмными язычками с S-образными косыми боками, точки столов, окна без рамки с зазорами 9 px, углами 10 и мягкой тенью, вместо анимаций — затухания, лаунчер 400 px с картинкой-шапкой, меню выключения из пяти крупных значков, блокировка Orbitron с падающими лепестками, JetBrains Mono везде.",
        geom={"gapsIn": 5, "gapsOut": 9, "borderSize": 0, "rounding": 10, "shadow": True},
        bar="cozytile", opacity="solid", blur="medium", anims="cozytile", lock="cozytile", launcher="cozytile",
        radius=8, alpha=1, cards="flat", fx={"type": "fade", "duration": 400, "easing": "OutCubic"},
        picker="cards", dash_anim="fade", sound_pack="paper", window_sounds=True, fonts="cozytile",
        attach="floating",
        look={"elevation": 1, "motion": 0.8, "material": "solid", "cornerScale": 0.6, "typeface": "shell"}),
    "surface": plain(
        "surface", "surface",
        "After surface-dots by snes19xx (its README allows reuse with credit): Everforest graphite or warm paper, a transparent top bar of pills with window icons, the Hub column under the clock, 1 px green window borders with corners of 7, windows popping in on springs, the serif Cassini power menu and the stellarium lock screen, Manrope in the shell.",
        "По мотивам surface-dots (snes19xx; README разрешает брать со ссылкой): графит или тёплая бумага Everforest, прозрачный бар сверху из пилюль со значками окон, колонка Hub под часами, рамки окон 1 px зеленью с углами 7, окна появляются на пружинах, меню выключения Cassini с засечками и экран блокировки stellarium, Manrope в оболочке.",
        geom={"gapsIn": 1, "gapsOut": 3, "borderSize": 1, "rounding": 7, "shadow": True},
        bar="surface", opacity="soft", blur="medium", anims="surface", lock="surface", launcher="surface",
        radius=16, alpha=1, cards="flat", fx={"type": "fade", "duration": 400, "easing": "OutCubic"},
        picker="cards", dash_anim="fade", sound_pack="fluent", window_sounds=True, fonts="surface",
        attach="floating",
        look={"elevation": 1, "motion": 1.0, "material": "solid", "cornerScale": 0.8, "typeface": "shell"}),
    "unit3": plain(
        "Unit-3", "Unit-3",
        "After Unit-3 by samyns (MIT, NieR:Automata): dark sepia with text in #c8b89a, a thin 28 px bar with workspace numbers, «// window title», a Japanese ticker and CPU / MEM / NET / VOL in muted colours, square windows with a 1 px border and no shadow or blur, its niercurve motion, Share Tech Mono everywhere.",
        "По мотивам Unit-3 (samyns, MIT, NieR:Automata): тёмная сепия с текстом #c8b89a, тонкий бар 28 px с номерами столов, «// заголовком окна», японской бегущей строкой и приглушёнными CPU / MEM / NET / VOL, квадратные окна с рамкой 1 px без тени и размытия, его кривая niercurve, Share Tech Mono везде.",
        geom={"gapsIn": 4, "gapsOut": 8, "borderSize": 1, "rounding": 0, "shadow": False},
        bar="unit3", opacity="solid", blur="off", anims="unit3", lock="unit3", launcher="unit3",
        radius=0, alpha=0.96, cards="bordered", fx={"type": "fade", "duration": 380, "easing": "OutCubic"},
        picker="nier", dash_anim="fade", sound_pack="retro", window_sounds=True, fonts="unit3",
        attach="floating",
        look={"elevation": 0, "motion": 0.9, "material": "solid", "cornerScale": 0, "typeface": "shell"}),
    "space": plain(
        "Space", "Space",
        "After the Space style of elifouts/Dotfiles (GPL-3.0): a No Man's Sky HUD — the wallpaper is a live landscape that pans when you switch workspaces, a thin bar of corner-bracketed boxes whose stars are the workspaces, uppercase spaced-out JetBrains Mono, windows without a border with an accent glow, see-through 0.8 / 0.7 over a light blur, its spring motion.",
        "По мотивам стиля Space из elifouts/Dotfiles (GPL-3.0): HUD в духе No Man's Sky — обои это живой пейзаж, который панорамирует при смене стола, тонкий бар из коробок с уголками, где звёзды — это столы, JetBrains Mono капсом и вразрядку, окна без рамки со свечением акцентом, прозрачность 0.8 / 0.7 над лёгким размытием, его пружинные анимации.",
        geom={"gapsIn": 4, "gapsOut": 12, "borderSize": 0, "rounding": 3, "shadow": False},
        bar="space", opacity="space", blur="space", anims="space", lock="space", launcher="space",
        radius=0, alpha=0.82, cards="bordered", fx={"type": "wipe", "duration": 900, "easing": "InOutSine"},
        picker="space", dash_anim="fade", sound_pack="neon", window_sounds=False, fonts="space",
        attach="floating",
        look={"elevation": 0, "motion": 1.0, "material": "glass", "cornerScale": 0, "typeface": "shell"}),
    "modern": plain(
        "Modern", "Modern",
        "After the Modern style of elifouts/Dotfiles (GPL-3.0): dark frosted glass over the wallpaper — colours from the wallpaper (pywal), windows without a border with corners of 10, see-through 0.78 / 0.7 over a blur and a soft shadow, bar pills that grow into cards on hover, a radial launcher, a home screen of cards, his fluid motion, Code New Roman.",
        "По мотивам стиля Modern из elifouts/Dotfiles (GPL-3.0): тёмное матовое стекло поверх обоев — цвета из обоев (pywal), окна без рамки со скруглением 10, прозрачность 0.78 / 0.7 над размытием и мягкая тень, пилюли бара вырастают в карточки при наведении, радиальный лаунчер, домашний экран из карточек, его плавные анимации, Code New Roman.",
        geom={"gapsIn": 2, "gapsOut": 10, "borderSize": 0, "rounding": 10, "shadow": True},
        bar="modern", opacity="modern", blur="modern", anims="modern", lock="modern", launcher="modern",
        radius=14, alpha=0.6, cards="modern", fx={"type": "fade", "duration": 500, "easing": "OutCubic"},
        picker="modern", dash_anim="fade", sound_pack="neon", window_sounds=False, fonts="modern",
        attach="floating",
        look={"elevation": 1, "motion": 1.0, "material": "glass", "cornerScale": 1, "typeface": "shell"}),
    "crt": plain(
        "Retro CRT", "Retro CRT",
        "After the Retro style of elifouts/Dotfiles (GPL-3.0): an old green-screen terminal — the whole screen goes through its CRT shader (Super+Alt+C), wallpapers are traced or dithered into the tube colour, a thin text bar of readouts, uppercase Terminess, square windows with a 1 px border in the tube colour, no blur or shadows, its sharp snap motion.",
        "По мотивам стиля Retro из elifouts/Dotfiles (GPL-3.0): старый терминал с зелёным экраном — весь экран идёт через его ЭЛТ-шейдер (Super+Alt+C), обои прорисованы или задизерены в цвет трубки, тонкий текстовый бар из показаний, Terminess капсом, квадратные окна с рамкой 1 px цветом трубки, без размытия и теней, его резкие анимации snap.",
        geom={"gapsIn": 3, "gapsOut": 8, "borderSize": 1, "rounding": 0, "shadow": False},
        bar="crt", opacity="solid", blur="off", anims="crt", lock="crt", launcher="crt",
        radius=0, alpha=0.86, cards="bordered", fx={"type": "fade", "duration": 400, "easing": "Linear"},
        picker="crt", dash_anim="fade", sound_pack="retro", window_sounds=False, fonts="crt",
        attach="floating",
        look={"elevation": 0, "motion": 1.0, "material": "solid", "cornerScale": 0, "typeface": "shell"}),

}

# Полнота: каждый стиль задаёт те же ручки, что и DOT-MATRIX, иначе переход между стилями будет неполным.
def shape(d):
    return {k: (sorted(v) if isinstance(v, dict) else None) for k, v in d.items()
            if k not in ("name", "name_ru", "note", "note_ru", "barSkin", "barSkinData", "barLayout", "barLayoutData")}

ref = shape(styles["dotmatrix"])
bad = False
for name, st in styles.items():
    sh = shape(st)
    for k in ref:
        if k not in sh:
            print(f"{name}: missing {k}"); bad = True
        elif ref[k] and set(ref[k]) - set(sh[k] or []):
            print(f"{name}.{k}: missing {sorted(set(ref[k]) - set(sh[k] or []))}"); bad = True
if bad:
    sys.exit(1)
# yami: своя раскладка бара (ячейки столов, шкалы), пиксельные часы и монитор из трёх карточек
styles["yami"]["barLayout"] = "yami"
styles["yami"]["widgets"].update(clockStyle="yami", sysinfoStyle="yami", mediaStyle="yami")
styles["rumda"]["barLayout"] = "rumda"
styles["rumda"]["widgets"].update(dashStyle="rumda")
styles["rumda"]["notifications"].update(notifyStyle="stock", notifyCards="rumda", notifyRadius=2, notifyWidth=300)
styles["bruteon"]["barLayout"] = "bruteon"
# стол как на его третьем скриншоте: часы с циферблатом и приветствием, плеер сверху по центру, карточка погоды
styles["bruteon"]["widgets"].update(dashStyle="bruteon", dashFollowBar=False, dashBackground="background",
                                    clockStyle="bruteon", mediaStyle="bruteon", mediaAnchor="top",
                                    weather=True)
styles["cozytile"]["barLayout"] = "cozytile"
# дашборд, Super+M, OSD и уведомления — фоном темы (его тёмная заливка), а не светлой заливкой бара
styles["cozytile"]["widgets"].update(dashFollowBar=False, dashBackground="background")
styles["cozytile"]["osd"].update(osdFollowBar=False, osdBackground="background")
styles["cozytile"]["notifications"].update(notifyFollowBar=False, notifyBackground="background")
styles["unit3"]["barLayout"] = "unit3"
# свои доски у yami, Cozytile и Glyph
styles["yami"]["widgets"].update(dashStyle="yami", dashFollowBar=False, dashBackground="background")
styles["cozytile"]["widgets"].update(dashStyle="cozytile")
styles["glyph"]["widgets"].update(dashStyle="glyph", dashFollowBar=False, dashBackground="background")
styles["unit3"]["widgets"].update(dashStyle="unit3", dashFollowBar=False, dashBackground="background", mediaStyle="default")
styles["unit3"]["notifications"].update(notifyStyle="stock", notifyCards="nier", notifyRadius=0, notifyWidth=360)
styles["surface"]["barLayout"] = "surface"
# Space: бар-коробки с уголками и звёздами-столами, визор-дашборд, карточки уведомлений с уголками
styles["space"]["barLayout"] = "space"
styles["space"]["widgets"].update(dashStyle="space", dashFollowBar=False, dashBackground="background", dashAlpha=0.4)
styles["space"]["notifications"].update(notifyStyle="stock", notifyCards="space", notifyRadius=0, notifyWidth=340,
                                         notifyCorner="bottom-left")
styles["space"]["osd"].update(osdStyle="space")  # его OSD: квадратная плашка внизу по центру (SpaceOsd.qml)
# Modern: пилюли бара с карточками, Home на весь экран, OSD и уведомления как у него
styles["modern"]["barLayout"] = "modern"
styles["modern"]["widgets"].update(dashStyle="modern", dashFollowBar=False, dashBackground="background",
                                    mediaAnchor="bottom-right")  # снизу слева — уведомления
styles["modern"]["osd"].update(osdStyle="modern")
styles["modern"]["notifications"].update(notifyStyle="stock", notifyCards="modern", notifyRadius=14, notifyWidth=380,
                                          notifyCorner="bottom-left")
# Retro CRT: текстовый бар, экран состояния, таблица окон, карточки уведомлений с двойной рамкой, шейдер трубки
styles["crt"]["barLayout"] = "crt"
styles["crt"]["osd"].update(osdStyle="crt")  # его OSD: плашка с клетками внизу по центру (CrtOsd.qml)
styles["liquid"]["osd"].update(osdStyle="vitreus")
styles["liquid"]["widgets"].update(mediaStyle="vitreus", clockStyle="vitreus", sysinfoStyle="vitreus")  # его плеер, часы «2/42» и кольца  # его OSD: капля из правой кромки с карандашной шкалой (VitreusOsd.qml)
styles["crt"]["shader"] = "retro-crt"
styles["crt"]["widgets"].update(dashStyle="crt", dashFollowBar=False, dashBackground="background", term=True, termAnchor="top-left")
styles["crt"]["notifications"].update(notifyStyle="stock", notifyCards="crt", notifyRadius=0, notifyWidth=380,
                                       notifyCorner="top-right")
styles["surface"]["widgets"].update(dashStyle="surface", powerStyle="auto", clockStyle="minimal")
for st in styles.values():
    st["widgets"].setdefault("sysinfoStyle", "rings")
    st["widgets"].setdefault("mediaStyle", "default")
    st["widgets"].setdefault("weather", False)
# Тема стиля (переключатель styleTheme): пара тёмная / светлая.
# у DOT-MATRIX и Glyph — одноцветные двойники тем (-mono); разноцветные остаются в списке тем
THEMES = {"dotmatrix": ("nothing-steel-mono", "nothing-ashlight-mono"), "glyph": ("nothing-glyph-dark-mono", "nothing-glyph-light-mono"), "flat": ("matte-black", "white"),
          "glass": ("catppuccin", "catppuccin-latte"), "liquid": ("catppuccin", "catppuccin-latte"), "fluent": ("tokyo-night", "rose-pine"),
          "paper": ("kanagawa", "kanagawa-lotus"), "neumorph": ("nord", "bliss"),
          "brutal": ("gruvbox-material", "flexoki-light"), "retro": ("ibm", "bliss"), "neon": ("cyber-aura", ""),
          "yami": ("yami-ash", ""), "rumda": ("rumda-dark", "rumda-light"), "surface": ("surface-dark", "surface-light"), "cozytile": ("cozytile-cozy", "cozytile-carbon"), "bruteon": ("bruteon-dark", "bruteon-light"), "unit3": ("unit3-dark", "unit3-paper"), "space": ("space-dusk", ""), "crt": ("crt-phosphor", ""), "modern": ("modern-default", "")}
for name, st in styles.items():
    dark, light = THEMES[name]
    st["theme"] = {"dark": dark, "light": light or dark}
# Части райса (дом, Deck, Super+M, меню выключения, буфер, обзор столов) — auto: вид выбирает сам виджет по райсу из style.json
# ("rice", пишет вкладка «Райсы»), а без райса — по стилю (Widgets.qml → partFor). Сменил райс — части подстроились.
PARTS = ("homeLayout", "homeCards", "deckLayout", "deckCards", "settingsPanel", "powerStyle", "clipboardPanel", "overviewStyle")
for name, st in styles.items():
    st["widgets"].update({k: "auto" for k in PARTS})
    st["widgets"].setdefault("term", False)  # терминал на обоях — только у Retro CRT, остальные стили его убирают
    st["widgets"].setdefault("termAnchor", "top-left")
for name, st in styles.items():
    with open(os.path.join(out, name + ".json"), "w") as f:
        json.dump(st, f, ensure_ascii=False, indent=2)
        f.write("\n")
print("ok:", ", ".join(styles))
