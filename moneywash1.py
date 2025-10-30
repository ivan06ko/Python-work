from typing import Callable, Generator, Iterable, Optional, Tuple

def parse_tx(line: str) -> Optional[Tuple[str, float]]:
    if not isinstance(line, str):
        return None
    parts = line.strip().split()
    if len(parts) != 2:
        return None
    kind, amount_s = parts[0].lower(), parts[1]
    if kind not in {"payment", "refund", "transfer"}:
        return None
    try:
        amount = float(amount_s)
    except ValueError:
        return None
    return kind, amount

def shadow(*, limit: float = 200.0) -> Callable[[Callable[..., Iterable[str]]], Callable[..., Generator[str, None, float]]]:
    def decorator(gen_func: Callable[..., Iterable[str]]) -> Callable[..., Generator[str, None, float]]:
        def wrapper(*args, **kwargs) -> Generator[str, None, float]:
            total = 0.0                     # накопичення
            over = False                    # стан "понад ліміт"
            gen = gen_func(*args, **kwargs) # оригінальний стрім

            for raw in gen:
                parsed = parse_tx(raw)
                if parsed is None:
                    # некоректне - ігноруємо 
                    continue

                kind, amount = parsed

                print(raw)

                if kind in {"payment", "transfer"}:
                    total += amount
                elif kind == "refund":
                    total -= amount

                if total > limit and not over:
                    print("Тіньовий ліміт перевищено. Активую схему")
                    over = True
                elif total <= limit and over:
                    over = False

                yield raw

            return round(total, 2)
        return wrapper
    return decorator

@shadow(limit=200)  # можна змінити ліміт тут
def tx_stream() -> Iterable[str]:
    # по черзі віддаємо сирі рядки
    data = [
        "payment 120",
        "refund 50",
        "qwerty 10",     # некоректне - ігнор
        "transfer 300",
        "refund X",      # некоректне - ігнор
        "payment 100",
        "refund 70",
        "transfer 50",
    ]
    for x in data:
        yield x

def run_and_get_total(gen: Generator[str, None, float]) -> float:
    # повністю виснажує генератор і беремо StopIteration.value
    while True:
        try:
            next(gen)
        except StopIteration as e:
            return e.value

if __name__ == "__main__":
    total = run_and_get_total(tx_stream())
    print(f"Фінальна сума: {total}")
