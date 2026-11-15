-- yami (по мотивам Trendorin/yami, MIT): короткие, чёткие анимации без размытия.
-- У yami окна проявляются и рассыпаются по клеткам 4 px (шейдеры niri window-open / window-close, 140 / 150 мс,
-- линейно); Hyprland шейдеров анимаций окон не умеет — здесь те же длительности и линейная кривая, окно появляется
-- почти в полный размер (popin 96 %) и проявляется затуханием. Столы и перемещения — жёсткие пружины yami
-- (damping 1.0, stiffness 900–1100) как быстрая кривая без перелёта.
hl.config({ animations = { enabled = true } })
hl.curve("linear", { type = "bezier", points = { { 0, 0 }, { 1, 1 } } })
hl.curve("yamiSnap", { type = "bezier", points = { { 0.25, 1 }, { 0.3, 1 } } })
hl.animation({ leaf = "windowsIn", enabled = true, speed = 1.4, bezier = "linear", style = "popin 96%" })
hl.animation({ leaf = "windowsOut", enabled = true, speed = 1.5, bezier = "linear", style = "popin 96%" })
hl.animation({ leaf = "windowsMove", enabled = true, speed = 1.6, bezier = "yamiSnap" })
hl.animation({ leaf = "fadeIn", enabled = true, speed = 1.4, bezier = "linear" })
hl.animation({ leaf = "fadeOut", enabled = true, speed = 1.5, bezier = "linear" })
hl.animation({ leaf = "fadeSwitch", enabled = true, speed = 1.2, bezier = "linear" })
hl.animation({ leaf = "fadeDim", enabled = true, speed = 1.2, bezier = "linear" })
hl.animation({ leaf = "fadeLayers", enabled = true, speed = 1.2, bezier = "linear" })
hl.animation({ leaf = "layers", enabled = true, speed = 1.2, bezier = "linear", style = "fade" })
hl.animation({ leaf = "border", enabled = true, speed = 1.0, bezier = "linear" })
hl.animation({ leaf = "workspaces", enabled = true, speed = 1.6, bezier = "yamiSnap", style = "slide" })
hl.animation({ leaf = "specialWorkspace", enabled = true, speed = 1.6, bezier = "yamiSnap", style = "slidevert" })
