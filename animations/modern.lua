-- Modern (elifouts/Dotfiles, GPL-3.0 — его Modern/base/style.lua): окна на кривой fluid (popin 5 %), закрытие и
-- затухание — snappy, столы — сдвигом, спецстол — slidefadevert −35 %, слои — popin 70 %.
hl.config({ animations = { enabled = true } })
hl.curve("fluid", { type = "bezier", points = { { 0.15, 0.85 }, { 0.25, 1 } } })
hl.curve("snappy", { type = "bezier", points = { { 0.3, 1 }, { 0.4, 1 } } })
hl.animation({ leaf = "windows", enabled = true, speed = 3, bezier = "fluid", style = "popin 5%" })
hl.animation({ leaf = "windowsOut", enabled = true, speed = 2.5, bezier = "snappy" })
hl.animation({ leaf = "fade", enabled = true, speed = 4, bezier = "snappy" })
hl.animation({ leaf = "workspaces", enabled = true, speed = 1.7, bezier = "snappy", style = "slide" })
hl.animation({ leaf = "specialWorkspace", enabled = true, speed = 4, bezier = "fluid", style = "slidefadevert -35%" })
hl.animation({ leaf = "layers", enabled = true, speed = 2, bezier = "snappy", style = "popin 70%" })
