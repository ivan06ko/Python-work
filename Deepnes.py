from abc import ABC, abstractmethod

class Transport(ABC): #класи дляя машинок
    def __init__(self, name: str, speed: int, capacity: int):
        self.name = name
        self.speed = speed
        self.capacity = capacity

    @abstractmethod # що ж це за абстрактний метод такий? 
    def move(self, distance: int) -> float:
        pass

    @abstractmethod
    def fuel_consumption(self, distance: int) -> float:
        pass

    @abstractmethod
    def info(self) -> str:
        pass

    def calculate_cost(self, distance: int, price_per_unit: float) -> float:
        return round(self.fuel_consumption(distance) * price_per_unit, 2)


class Car(Transport):
    def move(self, distance: int) -> float:
        return round(distance / self.speed, 2)

    def fuel_consumption(self, distance: int) -> float:
        return round(distance * 0.07, 2)

    def info(self) -> str:
        return f"Car {self.name}, speed: {self.speed}, capacity: {self.capacity}"


class Bus(Transport):
    def __init__(self, name: str, speed: int, capacity: int, passengers: int):
        super().__init__(name, speed, capacity)
        self.passengers = passengers

    def move(self, distance: int) -> float:
        return round(distance / self.speed, 2)

    def fuel_consumption(self, distance: int) -> float:
        if self.passengers > self.capacity:
            print("Перевантажено!")
        return round(distance * 0.15, 2)

    def info(self) -> str:
        return f"Bus {self.name}, speed: {self.speed}, passengers: {self.passengers}/{self.capacity}"


class Bicycle(Transport):
    def __init__(self, name: str, capacity: int = 1):
        super().__init__(name, 20, capacity)

    def move(self, distance: int) -> float:
        return round(distance / self.speed, 2)

    def fuel_consumption(self, distance: int) -> float:
        return 0.0

    def info(self) -> str:
        return f"Bicycle {self.name}, speed: {self.speed}"


class ElectricCar(Car):
    def battery_usage(self, distance: int) -> float:
        return round(distance * 0.2, 2)

    def fuel_consumption(self, distance: int) -> float:
        return 0.0

    def info(self) -> str:
        return f"ElectricCar {self.name}, speed: {self.speed}"


vehicles = [
    Car("Toyota", 120, 5),
    Bus("Ikarus", 80, 40, passengers=42),
    Bicycle("Crosswind"),
    ElectricCar("Tesla", 150, 5)
]

distance = 100
price = 60

for v in vehicles:
    print(v.info())
    print("Time:", v.move(distance))
    print("Fuel:", v.fuel_consumption(distance))
    if isinstance(v, ElectricCar):
        print("Battery:", v.battery_usage(distance))
    print("Cost:", v.calculate_cost(distance, price))
    print()