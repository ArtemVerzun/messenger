import QtQuick
import QtQuick.Window
import QtQuick.Controls

Label {
    property TextField field: null
    text: field.warning != '' ? field.warning : field.tip
    visible: true
    font.pointSize: 10
    color: field.warning != '' ? "red" : "#39fc03" // red : green
    anchors {
        bottom: field.top
        bottomMargin: 2
        left: field.left
        leftMargin: 3
    }
}