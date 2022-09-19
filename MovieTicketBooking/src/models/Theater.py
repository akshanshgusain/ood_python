from typing import List
from src.models.Screen import Screen


class Theater:
    def __init__(self, id: str, name: str):
        self.id: str = id
        self.name: str = name
        self.screens: List[Screen] = []

    def add_screen(self, screen: Screen):
        self.screens.append(screen)


