-- Retro CRT (elifouts/Dotfiles, GPL-3.0 — его Retro/base/style.lua): всё на резкой кривой snap, окна появляются
-- popin 96 %, закрываются по ступеньке step, слои — без движения (fade), столы — slidefade 8 %.
hl.config({ animations = { enabled = true } })
hl.curve("snap", { type = "bezier", points = { { 0.1, 0.9 }, { 0.2, 1 } } })
hl.curve("step", { type = "bezier", points = { { 0.7, 0 }, { 0.3, 1 } } })
hl.animation({ leaf = "global", enabled = true, speed = 3, bezier = "snap" })
hl.animation({ leaf = "windows", enabled = true, speed = 2.2, bezier = "snap", style = "popin 96%" })
hl.animation({ leaf = "windowsOut", enabled = true, speed = 1.4, bezier = "step", style = "popin 96%" })
hl.animation({ leaf = "fade", enabled = true, speed = 1.6, bezier = "snap" })
hl.animation({ leaf = "border", enabled = true, speed = 2, bezier = "snap" })
hl.animation({ leaf = "layers", enabled = true, speed = 2, bezier = "snap", style = "fade" })
hl.animation({ leaf = "workspaces", enabled = true, speed = 2.4, bezier = "snap", style = "slidefade 8%" })
