-- Bruteon (по мотивам райса-необрутализма Darkkal44 — по скриншотам, код свой): быстрые «упругие» появления — окно
-- выскакивает с 90 % с лёгким перелётом и так же уходит, перемещение — коротким пружинным рывком, столы — быстрым сдвигом.
hl.config({ animations = { enabled = true } })
hl.curve("bruteOvershot", { type = "bezier", points = { { 0.34, 1.56 }, { 0.64, 1 } } })
hl.curve("bruteSnap", { type = "bezier", points = { { 0.2, 0.9 }, { 0.1, 1 } } })
hl.animation({ leaf = "windowsIn", enabled = true, speed = 3, bezier = "bruteOvershot", style = "popin 90%" })
hl.animation({ leaf = "windowsOut", enabled = true, speed = 2.5, bezier = "bruteSnap", style = "popin 90%" })
hl.animation({ leaf = "windowsMove", enabled = true, speed = 3, bezier = "bruteOvershot", style = "slide" })
hl.animation({ leaf = "fade", enabled = true, speed = 2.5, bezier = "bruteSnap" })
hl.animation({ leaf = "layers", enabled = true, speed = 2.5, bezier = "bruteOvershot", style = "popin 90%" })
hl.animation({ leaf = "workspaces", enabled = true, speed = 3, bezier = "bruteSnap", style = "slide" })
hl.animation({ leaf = "border", enabled = false })
