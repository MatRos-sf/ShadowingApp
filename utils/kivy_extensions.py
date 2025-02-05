from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup


def message_box_info(message: str) -> None:
    """
    Display a popup message box with the provided message and a back button.
    """
    layout = BoxLayout(orientation="vertical", padding=10, spacing=10)

    # Content label
    content_label = Label(
        text=message, size_hint_y=None, halign="center", valign="middle"
    )
    content_label.bind(size=content_label.setter("text_size"))  # Allow text wrapping
    layout.add_widget(content_label)

    # Back button
    back_button = Button(text="Back", size_hint_y=None, height=40)
    back_button.bind(on_press=lambda instance: popup.dismiss())
    layout.add_widget(back_button)

    # Create the popup with dynamic sizing
    popup = Popup(
        title="Info",
        content=layout,
        size_hint=(None, None),
        size=(min(1000, content_label.width + 100), content_label.height + 100),
    )
    popup.open()
