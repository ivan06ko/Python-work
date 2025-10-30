from abc import ABC, abstractmethod
from typing import Type, Dict, Tuple

class Document(ABC):
    @abstractmethod
    def render(self) -> str:
        ...

#Конкретні документи 
class Report(Document):
    def __init__(self, title: str, summary: str):
        self.title = title
        self.summary = summary

    def render(self) -> str:
        return f"Звіт: {self.title}\nКоротко: {self.summary}\n"

class Invoice(Document):
    def __init__(self, number: str, amount: float, currency: str = "USD"):
        self.number = number
        self.amount = amount
        self.currency = currency

    def render(self) -> str:
        return f"Рахунок №{self.number}\nСума: {self.amount:.2f} {self.currency}\n"

class Contract(Document):
    def __init__(self, parties: Tuple[str, str], subject: str, terms: str):
        self.parties = parties
        self.subject = subject
        self.terms = terms

    def render(self) -> str:
        a, b = self.parties
        return (
            f"Договір: {a} — {b}\n"
            f"Предмет: {self.subject}\n"
            f"Умови: {self.terms}\n"
        )

# Null Object
class NullDocument(Document):
    def __init__(self, doc_type: str):
        self.doc_type = doc_type

    def render(self) -> str:
        return f"[Невідомий тип: '{self.doc_type}']\n"

# Фабрика
class DocumentFactory:
    _registry: Dict[str, Type[Document]] = {
        "report": Report,
        "invoice": Invoice,
        "contract": Contract,
    }

    @staticmethod
    def create(doc_type: str, strict: bool = False, **kwargs) -> Document:
        cls = DocumentFactory._registry.get((doc_type or "").lower())
        if cls is None:
            if strict:
                raise ValueError(f"Непідтримуваний тип: {doc_type}")
            return NullDocument(doc_type)
        return cls(**kwargs)

    @staticmethod
    def register(doc_type: str, cls: Type[Document]) -> None:
        DocumentFactory._registry[doc_type.lower()] = cls

# Наглядний приклад 
if __name__ == "__main__":
    documents = [
        DocumentFactory.create("report", title="Q3 2025", summary="Стабільне зростання."),
        DocumentFactory.create("invoice", number="INV-1024", amount=1999.99, currency="UAH"),
        DocumentFactory.create(
            "contract",
            parties=("ТОВ Альфа", "ТОВ Бета"),
            subject="Поставка серверів",
            terms="Оплата 30 днів."
        ),
        DocumentFactory.create("unknown_type"),
    ]

    for doc in documents:
        print(doc.render())