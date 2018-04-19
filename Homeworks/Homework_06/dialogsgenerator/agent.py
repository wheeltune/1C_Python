from collections import Generator


class Agent(Generator):
    def __init__(self, kb, name):
        self.kb = kb
        self.name = name

    def send(self, msg):
        # Необходимо написать свой собственный метод send для генератора
        return f"{self.name}: {self.kb.sample(1)['text'].values[0]}"

    def throw(self, typ=None, val=None, tb=None):
        # Оставляем как есть
        super().throw(typ, val, tb)

    def __str__(self):
        # Опишем строковое представление класса
        return f"Agent({self.name})"

    def __repr__(self):
        return str(self)
