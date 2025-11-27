import threading
import time
import random


# Склад з медикаментами
class Warehouse:
    def __init__(self, name, meds):
        self.name = name
        self.meds = meds
        self.lock = threading.Lock()

    def steal(self, amount):
        # 1 - піймали, 2 - лохи, 3 - ура зробили
        outcome = random.randint(1, 3)

        if outcome == 1:
            return -1  # спіймали

        if outcome == 2:
            return 0   # нічого не вкрали

        if self.meds <= 0:
            return 0

        max_can_take = min(amount, self.meds)
        stolen = random.randint(1, max_can_take)
        self.meds -= stolen
        return stolen


# Бігун (потік)
class Runner(threading.Thread):
    price_per_unit = 5

    def __init__(self, name, warehouse):
        super().__init__()
        self.name = name
        self.warehouse = warehouse
        self.earned = 0
        self.attempts = 10
        self.done = 0
        self.caught = False

    def run(self):
        for i in range(self.attempts):
            time.sleep(random.uniform(0.1, 0.5))
            amount = random.randint(10, 30)

            with self.warehouse.lock:
                result = self.warehouse.steal(amount)

            if result == -1:
                self.caught = True
                self.done = i + 1
                break
            elif result > 0:
                self.earned += result * self.price_per_unit

            self.done = i + 1


def show_progress(runners):
    print("\nПрогрес бігунів:")
    for r in runners:
        bar_len = 20 #test test test. is it working?
        filled = int(bar_len * r.done / r.attempts)
        bar = "#" * filled + "." * (bar_len - filled)

        if r.caught:
            status = "спійманий"
        elif r.done == r.attempts:
            status = "готово"
        else:
            status = "в процесі"

        print(f"{r.name:10} [{bar}] {r.done:2}/{r.attempts}  {status}")


def run_simulation(number, num_runners=5):
    print(f"\n=== СИМУЛЯЦІЯ {number} ===")

    warehouses = [
        Warehouse("Склад A", random.randint(100, 300)),
        Warehouse("Склад B", random.randint(100, 300)),
        Warehouse("Склад C", random.randint(100, 300)),
        Warehouse("Склад D", random.randint(100, 300)),
        Warehouse("Склад E", random.randint(100, 300)),
    ]

    runners = []
    for i in range(num_runners):
        w = random.choice(warehouses)
        runners.append(Runner(f"Бігун {i + 1}", w))

    for r in runners:
        r.start()

    while any(r.is_alive() for r in runners):
        show_progress(runners)
        time.sleep(0.3)

    for r in runners:
        r.join()

    show_progress(runners)

    print("\nПідсумок по бігунах:")
    total_earned = 0
    for r in runners:
        status = "спійманий" if r.caught else "вижив"
        print(f"{r.name:10} заробив: {r.earned:4}  | {status}")
        total_earned += r.earned

    print("\nЗалишок медикаментів:")
    for w in warehouses:
        print(f"{w.name:10}: {w.meds} одиниць")

    print(f"\nЗагальний заробіток: {total_earned}")


if __name__ == "__main__":
    for i in range(1, 3 + 1):
        run_simulation(i)
        time.sleep(1)   