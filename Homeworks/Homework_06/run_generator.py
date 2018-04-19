from dialogsgenerator import RandomDialog, Agent
import pandas as pd
import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument("count_dialogs", type=int,
                    help="Количество диалогов, которые необходимо сгенерировать.")
parser.add_argument("max_dialog_len", type=int,
                    help="Максимальное количество цепочек в одном диалоге.")
parser.add_argument("-o", "--output",
                    help="Поток, в который будет производиться вывод",
                    default=sys.stdout)
parser.add_argument("-t", "--trump_kb", type=str,
                    help="Файл с репликами ответов Трампа.",
                    default="trump.csv")
parser.add_argument("-c", "--clinton_kb", type=str,
                    help="Файл с репликами ответов Клинтон.",
                    default="clinton.csv")


def generate(rd, count_dialogs=5):
    """
    Генерирует count_dialogs диалогов с помощью rd.generate().
    Возвращаемый объект является генератором.
    """
    yield map(lambda _: list(next(rd.generate())), range(count_dialogs))


def write(dialogs, target):
    """
    Записывает сгенерированные диалоги dialogs (это объект-генератор) в поток target.
    """
    target.write("\n\n".join(map(lambda dialog: f"--------------------------------------------------Dialog {dialog[0]}"
                                                f"--------------------------------------------------\n\n" +
                                                f"\n\n".join(map(lambda turn: f"Turn {turn[0]}:\n\t" +
                                                                              "\n\t".join(turn[1]),
                                                                 enumerate(dialog[1]))), enumerate(next(dialogs)))))


if __name__ == "__main__":
    args = parser.parse_args()
    is_opened = False
    if isinstance(args.output, str):
        args.output = open(args.output, "w")
        is_opened = True

    trump = pd.read_csv(args.trump_kb, encoding="utf-8")
    clinton = pd.read_csv(args.clinton_kb, encoding="utf-8")

    rd = RandomDialog([Agent(clinton, "clinton"), Agent(trump, "trump")], args.max_dialog_len)
    write(generate(rd, args.count_dialogs), args.output)

    if is_opened:
        args.output.close()
