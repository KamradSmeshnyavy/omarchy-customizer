import QtQuick
import QtQuick.Effects
import Quickshell
import Quickshell.Io
import Quickshell.Wayland

// Переход при смене райса — по мотивам его utilities/session/TransitionShared.qml (github.com/elifouts/Dotfiles,
// GPL-3.0; код свой): отдельный процесс quickshell (`scripts/rice-transition.sh begin`), живёт, пока Customizer
// применяет райс. Кадр экрана замирает (ScreencopyView без live) и уходит под размытие, по центру полоса загрузки
// цветом акцента старой темы и имя райса; `reveal` — полоса добегает, кадр тает, процесс выходит. Если reveal так и
// не пришёл — сам уходит через 40 с. Клики и клавиатуру не берёт.
//
// boot — заставка при входе для райсов без своей: чёрный экран, из него проявляются размытые обои, имя райса и полоса,
// потом всё тает (`rice-transition.sh boot`).
ShellRoot {
  id: root

  readonly property string mode: Quickshell.env("RICE_TRANSITION_MODE") || "switch"
  readonly property string label: Quickshell.env("RICE_TRANSITION_LABEL") || ""
  readonly property bool boot: mode === "boot"
  readonly property int fade: 420

  // цвета текущей темы (colors.toml); до чтения — белый, как у него
  property color accent: "white"
  property color fg: "white"
  property color bg: "black"
  FileView {
    path: Quickshell.env("HOME") + "/.local/state/omarchy/current/theme/colors.toml"
    printErrors: false
    onLoaded: {
      const t = text()
      function pick(k) { const m = t.match(new RegExp("^\\s*" + k + "\\s*=\\s*\"(#[0-9a-fA-F]{6})", "m")); return m ? m[1] : "" }
      if (pick("accent")) root.accent = pick("accent")
      if (pick("foreground")) root.fg = pick("foreground")
      if (pick("background")) root.bg = pick("background")
    }
  }

  property int captured: 0
  property bool revealing: false
  property real progress: 0
  property real shown: 0
  NumberAnimation on progress { running: !root.revealing && (root.boot || root.captured > 0); to: 0.9; duration: root.boot ? 1600 : 1400; easing.type: Easing.OutCubic }
  NumberAnimation on progress { running: root.revealing; to: 1; duration: 160 }
  NumberAnimation on shown { running: root.boot; from: 0; to: 1; duration: 1100; easing.type: Easing.InOutCubic }

  function reveal() { if (!revealing) { revealing = true; done.start() } }
  IpcHandler {
    target: "transition"
    function covered(): bool { return root.boot || root.captured >= Quickshell.screens.length }
    function reveal(): void { root.reveal() }
  }
  Timer { interval: root.boot ? 2600 : 40000; running: !root.revealing; onTriggered: root.reveal() }
  Timer { id: done; interval: root.fade + 60; onTriggered: Qt.quit() }

  Variants {
    model: Quickshell.screens
    PanelWindow {
      id: win
      required property var modelData
      screen: modelData
      anchors { top: true; bottom: true; left: true; right: true }
      exclusionMode: ExclusionMode.Ignore
      color: "transparent"
      mask: Region {}
      WlrLayershell.layer: WlrLayer.Overlay
      WlrLayershell.namespace: "rice-transition"
      WlrLayershell.keyboardFocus: WlrKeyboardFocus.None

      Item {
        anchors.fill: parent
        OpacityAnimator on opacity { running: root.revealing; to: 0; duration: root.fade; easing.type: Easing.InOutSine }

        // смена: застывший кадр под размытием
        ScreencopyView {
          id: frame
          anchors.fill: parent
          visible: !root.boot
          captureSource: root.boot ? null : win.modelData
          live: false
          paintCursor: false
          onHasContentChanged: if (hasContent) root.captured++
        }
        MultiEffect {
          anchors.fill: parent
          visible: !root.boot && frame.hasContent
          source: frame
          autoPaddingEnabled: false
          blurEnabled: true
          blurMax: 48
          blur: frame.hasContent ? 1 : 0
          brightness: frame.hasContent ? -0.12 : 0
          Behavior on blur { NumberAnimation { duration: 180; easing.type: Easing.OutCubic } }
          Behavior on brightness { NumberAnimation { duration: 180 } }
        }

        // заставка: из чёрного проявляются размытые обои
        Rectangle { anchors.fill: parent; visible: root.boot; color: "black" }
        Image {
          id: wall
          anchors.fill: parent
          visible: false
          source: root.boot ? "file://" + Quickshell.env("HOME") + "/.local/state/omarchy/current/background" : ""
          sourceSize.width: 1280
          fillMode: Image.PreserveAspectCrop
          asynchronous: true
          cache: false
        }
        MultiEffect {
          anchors.fill: parent
          visible: root.boot
          source: wall
          blurEnabled: true; blur: 1; blurMax: 64
          brightness: -0.2
          opacity: root.shown
          scale: 1.04 - 0.04 * root.shown
        }

        Column {
          anchors.centerIn: parent
          spacing: 14
          opacity: root.boot ? root.shown : frame.hasContent ? 1 : 0
          Behavior on opacity { enabled: !root.boot; NumberAnimation { duration: 140 } }
          Text {
            visible: root.label !== ""
            anchors.horizontalCenter: parent.horizontalCenter
            text: root.label.toUpperCase()
            color: root.fg
            opacity: 0.85
            font.pixelSize: 15
            font.letterSpacing: 5
          }
          Rectangle {
            anchors.horizontalCenter: parent.horizontalCenter
            width: 220; height: 4; radius: 2
            color: Qt.rgba(root.fg.r, root.fg.g, root.fg.b, 0.18)
            Rectangle { width: parent.width * root.progress; height: parent.height; radius: parent.radius; color: root.accent }
          }
        }
      }
    }
  }
}
