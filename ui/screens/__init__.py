from pathlib import Path

from kivy.lang.builder import Builder

KIVY_FILE = Path(__file__).parent.parent / Path("kv") / Path("main_screen.kv")
Builder.load_file(str(KIVY_FILE))
