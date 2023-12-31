import QtQuick
import QtQuick.Window
import QtQuick.Controls

Rectangle {
    id: titleBar

    property string title: "Window"
    property bool minimizable: true
    property bool maximizable: true
    property bool closable: true

    DragHandler { onActiveChanged: if (active) window.startSystemMove() }

    height: 30
    anchors {
        left: parent.left
        right: parent.right
        top: parent.top
    }
    color: "#24292e"
    // WINDOW BUTTONS
    Row {
        id: windowButtons
        width: 90
        layoutDirection: Qt.RightToLeft
        anchors {
            right: parent.right
            top: parent.top
            bottom: parent.bottom
        }

        TemplateButton {
            id: closeButton
            visible: closable
            width: parent.width / 3; height: parent.height;
            colorMouseOver: "#f50000"
            colorClicked: "#ba3b32"
            onClicked: windowManager.exit()
            iconSource: "../resources/icons/close.png"
        }

        TemplateButton {
            id: maximizeButton
            width: parent.width / 3; height: parent.height;
            visible: false
            iconHeight: 35
            iconWidth: 35
            colorMouseOver: "#61875d"
            colorClicked: "#5fba56"
            //onClicked: controller.closeApplication()
            iconSource: "../resources/icons/maximize.png"
        }
        TemplateButton {
            id: minimizeButton
            visible: false
            width: parent.width / 3; height: parent.height;
            colorMouseOver: "#616161"
            colorClicked: "#805db0"
            //onClicked: controller.closeCurrentWindow()
            iconSource: "../resources/icons/minimize.png"
        }


    }
    // WINDOW TITLE
    Rectangle {
        id: windowTitle
        color: "transparent"
        anchors {
            left: parent.left
            right: windowButtons.left
            top: parent.top
            bottom: parent.bottom
        }

        Label {
            color: "white"
            anchors {
                left: parent.left
                verticalCenter: parent.verticalCenter
                leftMargin: 30
            }
            text: "verzunMessenger"
            horizontalAlignment: Text.AlignLeft
            verticalAlignment: Text.AlignVCenter
            font.weight: Font.Medium
            font.pointSize: 10
            font.family: "Arial"
            styleColor: "#e3f0f2"
        }

        Image {
            id: logo
            width: 20
            height: 20
            anchors {
                left: parent.left
                verticalCenter: parent.verticalCenter
                leftMargin: 5
            }
            source: "../resources/images/logo.png"
         }
    }
}
