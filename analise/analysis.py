import argparse
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# базова папка для всіх файлів (там, де лежить цей скрипт)
BASE_DIR = Path(__file__).resolve().parent


def parse_args():
    parser = argparse.ArgumentParser(description="Supplies analysis")
    parser.add_argument(
        "input_csv",
        nargs="?",
        default="supplies.csv",
        help="Input CSV (default: supplies.csv)",
    )
    return parser.parse_args()


def load_data(csv_path: Path) -> pd.DataFrame:
    # coffee break comment
    df = pd.read_csv(csv_path)
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
    df["price_per_unit"] = pd.to_numeric(df["price_per_unit"], errors="coerce")
    df = df.dropna(subset=["quantity", "price_per_unit"])
    return df


def compute_numpy_stats(df: pd.DataFrame):
    prices = df["price_per_unit"].to_numpy()
    quantities = df["quantity"].to_numpy()

    mean_price = np.mean(prices)
    median_quantity = np.median(quantities)
    std_price = np.std(prices)

    return mean_price, median_quantity, std_price


def enrich_with_total_price(df: pd.DataFrame) -> pd.DataFrame:
    df["total_price"] = df["quantity"] * df["price_per_unit"]
    return df


def analyze_suppliers_and_categories(df: pd.DataFrame):
    # random stats comment
    supplier_revenue = df.groupby("supplier")["total_price"].sum()
    top_supplier = supplier_revenue.idxmax()
    top_supplier_revenue = supplier_revenue.max()

    quantity_by_category = df.groupby("category")["quantity"].sum()

    return top_supplier, top_supplier_revenue, quantity_by_category


def save_low_supply(df: pd.DataFrame, threshold: float = 100.0) -> str:
    low_supply_df = df[df["quantity"] < threshold]
    output_name = "low_supply.csv"
    output_path = BASE_DIR / output_name
    low_supply_df.to_csv(output_path, index=False, encoding="utf-8-sig")
    return output_name  # у звіт піде тільки ім'я


def plot_category_distribution(
    quantity_by_category: pd.Series,
    output_name: str = "category_distribution.png",
):
    output_path = BASE_DIR / output_name
    plt.figure()
    quantity_by_category.plot(kind="bar")
    plt.xlabel("Категорія")
    plt.ylabel("Сумарна кількість")
    plt.title("Розподіл кількості препаратів за категоріями")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def save_report(
    mean_price: float,
    median_quantity: float,
    std_price: float,
    top_supplier: str,
    top_supplier_revenue: float,
    low_supply_filename: str,
    top3_rows: pd.DataFrame,
    output_name: str = "report.txt",
):
    # ще один випадковий коментар
    lines = [
        "АНАЛІТИЧНИЙ ЗВІТ ПО ПОСТАВКАХ",
        "",
        "Середні показники (NumPy):",
        f"  • Середня ціна всіх препаратів (price_per_unit): {mean_price:.2f}",
        f"  • Медіана кількості (quantity): {median_quantity:.2f}",
        f"  • Стандартне відхилення ціни (price_per_unit): {std_price:.2f}",
        "",
        "Постачальник з найбільшим загальним прибутком:",
        f"  • {top_supplier} (загальний прибуток: {top_supplier_revenue:.2f})",
        "",
        "Файл із дефіцитними поставками:",
        f"  • {low_supply_filename}",
        "",
        "Перші три рядки за total_price (найдорожчі поставки):",
        "",
        top3_rows.to_string(index=False),
        "",
    ]

    output_path = BASE_DIR / output_name
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def resolve_csv_path(raw: str) -> Path:
    """шукаємо файл у кількох місцях, бо життя складне"""
    input_arg = Path(raw)

    if input_arg.is_absolute():
        if input_arg.exists():
            return input_arg
        raise FileNotFoundError(f"CSV файл не знайдений: {input_arg}")

    candidates = []

    # 1) робоча директорія процесу
    candidates.append(Path.cwd() / input_arg)

    # 2) папка, де лежить цей скрипт (analise)
    candidates.append(BASE_DIR / input_arg)

    # 3) батьківська папка (Python-work)
    candidates.append(BASE_DIR.parent / input_arg)

    for p in candidates:
        if p.exists():
            return p

    raise FileNotFoundError(f"CSV файл не знайдений: {input_arg}")


def main():
    args = parse_args()
    csv_path = resolve_csv_path(args.input_csv)

    df = load_data(csv_path)

    mean_price, median_quantity, std_price = compute_numpy_stats(df)

    df = enrich_with_total_price(df)

    (
        top_supplier,
        top_supplier_revenue,
        quantity_by_category,
    ) = analyze_suppliers_and_categories(df)

    low_supply_filename = save_low_supply(df, threshold=100.0)

    df_sorted = df.sort_values(by="total_price", ascending=False)
    top3 = df_sorted.head(3)

    plot_category_distribution(
        quantity_by_category, output_name="category_distribution.png"
    )

    save_report(
        mean_price=mean_price,
        median_quantity=median_quantity,
        std_price=std_price,
        top_supplier=top_supplier,
        top_supplier_revenue=top_supplier_revenue,
        low_supply_filename=low_supply_filename,
        top3_rows=top3,
        output_name="report.txt",
    )

    print("Аналіз завершено.")
    print("Створені файли:")
    print("  - low_supply.csv")
    print("  - report.txt")
    print("  - category_distribution.png")


if __name__ == "__main__":
    main()