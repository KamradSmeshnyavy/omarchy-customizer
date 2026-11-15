-- Cozytile (по мотивам Darkkal44/Cozytile — облик, код свой): у него анимаций окон нет, только затухание picom
-- (fade-in/out step 0.03 раз в 5 мс ≈ 165 мс). Окна и слои проявляются и гаснут на месте, без сдвига и масштаба,
-- столы сменяются тем же затуханием.
hl.config({ animations = { enabled = true } })
hl.curve("cozyLinear", { type = "bezier", points = { { 0, 0 }, { 1, 1 } } })
hl.curve("cozyEase", { type = "bezier", points = { { 0.25, 0.1 }, { 0.25, 1 } } })
hl.animation({ leaf = "windows", enabled = true, speed = 2, bezier = "cozyEase", style = "popin 100%" })
hl.animation({ leaf = "windowsMove", enabled = true, speed = 2.5, bezier = "cozyEase" })
hl.animation({ leaf = "fadeIn", enabled = true, speed = 1.65, bezier = "cozyLinear" })
hl.animation({ leaf = "fadeOut", enabled = true, speed = 1.65, bezier = "cozyLinear" })
hl.animation({ leaf = "fadeSwitch", enabled = true, speed = 1.65, bezier = "cozyLinear" })
hl.animation({ leaf = "fadeLayersIn", enabled = true, speed = 1.65, bezier = "cozyLinear" })
hl.animation({ leaf = "fadeLayersOut", enabled = true, speed = 1.65, bezier = "cozyLinear" })
hl.animation({ leaf = "layers", enabled = true, speed = 2, bezier = "cozyEase", style = "fade" })
hl.animation({ leaf = "workspaces", enabled = true, speed = 1.65, bezier = "cozyLinear", style = "fade" })
hl.animation({ leaf = "border", enabled = false })
