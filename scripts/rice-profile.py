#!/usr/bin/python3 -I
"""Быстрая смена профиля текущего райса (Super+Alt+P / Super+Alt+Shift+P).

  rice-profile.py next | prev    следующий / предыдущий профиль
  rice-profile.py list           профили текущего райса (имя, путь), текущий помечен *

Профили райса — его варианты / profiles из rices.json и свои сохранённые (поле "rice" в пресете), как в панели
настроек. Не райс — пишет об этом уведомлением. Применяется как пресет (apply_ops.apply_preset)."""
import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "backend"))

from customizer import apply_ops, state  # noqa: E402
from customizer.i18n import t  # noqa: E402


def profiles(rid):
    r = next((x for x in state.rices() if x["id"] == rid), None)
    out = []
    if r:
        for stem in r.get("profiles") or [v["preset"] for v in r["variants"]]:
            p = state.PRESET_DIR / f"{stem}.json"
            if p.is_file():
                out.append((stem, p))
    if state.USER_PRESETS.is_dir():
        for p in sorted(state.USER_PRESETS.glob("*.json")):
            try:
                if json.loads(p.read_text()).get("rice") == rid:
                    out.append((p.stem, p))
            except (OSError, ValueError):
                pass
    return out


def notify(body):
    subprocess.Popen(["notify-send", "-a", "Customizer", "-t", "2500", t("Profile"), body],
                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def main():
    what = sys.argv[1] if len(sys.argv) > 1 else "next"
    rid = state.current_rice()
    ps = profiles(rid) if rid else []
    try:
        cur = state.ACTIVE_PRESET.read_text().strip()
    except OSError:
        cur = ""
    if what == "list":
        for stem, p in ps:
            print(("* " if stem == cur else "  ") + state.preset_name(str(p)) + "\t" + str(p))
        return 0
    if len(ps) < 2:
        notify(t("This rice has no other profiles") if rid else t("No rice is active"))
        return 0
    i = next((k for k, (stem, _) in enumerate(ps) if stem == cur), -1)
    i = (i + (1 if what != "prev" else -1)) % len(ps)
    notify(f"{state.preset_name(str(ps[i][1]))}  ·  {i + 1}/{len(ps)}")
    apply_ops.apply_preset(str(ps[i][1]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
