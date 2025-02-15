from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView


def message_box_info(message: str) -> None:
    """
    Display a popup message box with the provided message and a back button.
    """
    layout = BoxLayout(orientation="vertical", padding=10, spacing=10)

    # Scroll text area
    scroll_view = ScrollView(size_hint=(1, None), height=300)

    # Content label
    content_label = Label(
        text=message,
        size_hint_y=None,
        halign="center",
        valign="top",
        text_size=(400, None),
    )
    content_label.bind(
        texture_size=lambda instance, value: setattr(instance, "height", value[1])
    )  # Allow text wrapping
    scroll_view.add_widget(content_label)
    layout.add_widget(scroll_view)

    # Back button
    back_button = Button(text="Back", size_hint_y=None, height=40)
    back_button.bind(on_press=lambda instance: popup.dismiss())
    layout.add_widget(back_button)

    # Create the popup with dynamic sizing
    popup = Popup(
        title="Info",
        content=layout,
        size_hint=(0.8, 0.8),  # Use size_hint for dynamic sizing
        auto_dismiss=True,
    )
    popup.open()
