#!/bin/bash
# Переход при смене райса (по мотивам utilities/session/transition.sh из elifouts/Dotfiles, GPL-3.0; код свой).
#   rice-transition.sh begin [имя]   застывший кадр под размытием с полосой загрузки (ждёт, пока кадр снят)
#   rice-transition.sh reveal        полоса добегает, кадр тает, оверлей выходит
#   rice-transition.sh boot [имя]    заставка при входе: из чёрного — размытые обои, имя райса, полоса
# Оверлей — отдельный процесс quickshell (transition/shell.qml), поэтому переживает перезагрузку плагинов шелла.
set -uo pipefail

QML="$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")/../transition" && pwd)/shell.qml"
# флаг для плагина уведомлений: 1 — переход идёт, тосты не показывать (оверлей не может лечь поверх новых слоёв)
FLAG="${XDG_RUNTIME_DIR:-/tmp}/omarchy-rice-transition"
call() { qs -p "$QML" ipc call transition "$@" 2>/dev/null; }

start() {
  qs kill -p "$QML" </dev/null >/dev/null 2>&1
  RICE_TRANSITION_MODE="$1" RICE_TRANSITION_LABEL="${2:-}" QSG_USE_SIMPLE_ANIMATION_DRIVER=1 \
    qs -n -p "$QML" --daemonize </dev/null >/dev/null 2>&1
}

case "${1:-}" in
  begin)
    echo 1 > "$FLAG"
    start switch "${2:-}"
    # кадр должен застыть до того, как что-то поменяется (до 1,2 с)
    for _ in $(seq 1 60); do
      [ "$(call covered)" = true ] && break
      sleep 0.02
    done
    ;;
  reveal)
    # плагины шелла перерисовываются после применения — дать им кадр-другой
    sleep 0.6
    call reveal
    sleep 0.5
    echo 0 > "$FLAG"
    ;;
  boot)
    start boot "${2:-}"
    ;;
  *)
    echo "usage: rice-transition.sh begin [label] | reveal | boot [label]" >&2
    exit 2
    ;;
esac
exit 0
