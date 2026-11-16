-- Unit-3 (samyns/Unit-3, MIT — его hyprland.conf): одна кривая niercurve (0.4, 0, 0.2, 1) — окна въезжают и уезжают
-- сдвигом (4 / 3), затухание 4, столы — вертикальным сдвигом 5.
hl.config({ animations = { enabled = true } })
hl.curve("niercurve", { type = "bezier", points = { { 0.4, 0 }, { 0.2, 1 } } })
hl.animation({ leaf = "windows", enabled = true, speed = 4, bezier = "niercurve", style = "slide" })
hl.animation({ leaf = "windowsOut", enabled = true, speed = 3, bezier = "niercurve", style = "slide" })
hl.animation({ leaf = "fade", enabled = true, speed = 4, bezier = "niercurve" })
hl.animation({ leaf = "workspaces", enabled = true, speed = 5, bezier = "niercurve", style = "slidevert" })
