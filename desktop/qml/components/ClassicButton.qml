import Qt5Compat.GraphicalEffects
import "../templates"

TemplateButton {
    buttonText: "Кнопка"
    height: 40
    width: 200
    fontSize: 14
    buttonRadius: 7
    colorDefault: "#24292e"
    colorMouseOver: "#212529"
    colorClicked: "#212529"
    layer.enabled: true
    layer.effect: DropShadow {
        transparentBorder: true
        horizontalOffset: 2
        verticalOffset: 2
        color: "#50000000"
    }
}