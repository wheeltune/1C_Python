import random
import sys


class RandomDialog(object):
    def __init__(self, agents, max_len=5):
        # Инициализация
        self.agents = agents
        self.max_len = max_len

    def generate(self):
        """
        Генерирует случайный диалог состоящий из 1-max_len цепочек.
        При генерации вызывает функцию turn.
        Возвращаемый объект является генератором.
        """
        yield map(lambda _: list(self.turn()), range(self.max_len))

    def turn(self):
        """
        Генерирует одну случайную цепочку следующим образом: выбирается случайный агент.
        Он "говорит" случайное сообщение (msg) из своей Agent.kb (используйте next или send(None)).
        (правила того, как выбирать никак не регулируются, вы можете выбирать случайный твит из Agent.kb никак не учитывая
        переданное msg).
        Это сообщение передается с помощью send (помним, что агент - это объект-генератор).
        Далее получаем ответ от всех агентов и возвращаем (генерируем) их (включая исходное сообщение).
        Возвращаемый объект является генератором.
        """
        rnd_index = random.randint(0, len(self.agents) - 1)
        statement = self.agents[rnd_index].send(None)
        yield statement
        yield from map(lambda index: self.agents[index].send(statement), range(len(self.agents)))

    def eval(self, dialog=None):
        """
        Превращает генератор случайного далога (который возвращается в self.generate())
        в список списков (пример использования далее).
        Возвращаемый объект является списком.
        """
        if dialog is None:
            dialog = self.generate()

        return list(next(dialog))

    def write(self, dialog=None, target=sys.stdout):
        """
        Записывает результат self.eval() в соответствующий поток.
        """
        if dialog is None:
            dialog = self.eval()

        target.write("\n".join(map(lambda turn: f"Turn {turn[0]}:\n\t" + "\n\t".join(turn[1]),
                                   enumerate(dialog))))
