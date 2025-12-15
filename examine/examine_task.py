import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd


class FIIncViewer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("FI-INC — Offline Incident Viewer")
        self.geometry("900x520")

        self.df = None 
        self._build_ui()

    def _build_ui(self):
        bar = ttk.Frame(self, padding=8)
        bar.pack(fill="x")

        ttk.Button(bar, text="Open CSV", command=self.open_csv).pack(side="left")
        ttk.Label(bar, text="Search:").pack(side="left", padx=(12, 4))

        self.q = tk.StringVar()
        ttk.Entry(bar, textvariable=self.q, width=28).pack(side="left")
        ttk.Button(bar, text="Apply", command=self.apply_search).pack(side="left", padx=6)
        ttk.Button(bar, text="Reset", command=self.reset).pack(side="left")

        area = ttk.Frame(self, padding=(8, 0, 8, 8))
        area.pack(fill="both", expand=True)

        self.tree = ttk.Treeview(area, show="headings")
        y = ttk.Scrollbar(area, orient="vertical", command=self.tree.yview)
        x = ttk.Scrollbar(area, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=y.set, xscrollcommand=x.set)

        self.tree.pack(side="left", fill="both", expand=True)
        y.pack(side="right", fill="y")
        x.pack(side="bottom", fill="x")

        self.status = tk.StringVar(value="Open a CSV file…")
        ttk.Label(self, textvariable=self.status, padding=8).pack(fill="x")

    def open_csv(self):
        path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
        if not path:
            return

        try:
            df = self._read_csv_safe(path)
            if df.empty or len(df.columns) == 0:
                raise ValueError("Empty or invalid table.")
            df.columns = [str(c).strip() for c in df.columns]
            self.df = df
            self.q.set("")
            self.show(df)
            self.status.set(f"Loaded: {len(df)} rows, {len(df.columns)} columns")
        except Exception as e:
            messagebox.showerror("File error", f"Cannot open CSV:\n{e}")
            self.status.set("Load failed")

    def _read_csv_safe(self, path: str) -> pd.DataFrame:
        for enc in ("utf-8", "utf-8-sig", "cp1251"):
            try:
                return pd.read_csv(path, encoding=enc)
            except Exception:
                pass
        raise ValueError("Failed to read CSV (bad encoding/format).")

    # ---- view ----
    def show(self, df: pd.DataFrame):
        self.tree.delete(*self.tree.get_children())
        cols = list(df.columns)
        self.tree["columns"] = cols

        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=140, stretch=True)

        for _, row in df.head(3000).iterrows():
            self.tree.insert("", "end", values=[self._cell(row.get(c)) for c in cols])

    @staticmethod
    def _cell(v):
        if pd.isna(v):
            return ""
        s = str(v)
        return s if len(s) <= 200 else s[:200] + "…"

    def apply_search(self):
        if self.df is None:
            return
        q = self.q.get().strip()
        if not q:
            self.reset()
            return

        mask = None
        for c in self.df.columns:
            part = self.df[c].astype(str).str.contains(q, case=False, na=False)
            mask = part if mask is None else (mask | part)

        view = self.df[mask]
        self.show(view)
        self.status.set(f"Filtered by '{q}': {len(view)} rows")

    def reset(self):
        if self.df is None:
            return
        self.q.set("")
        self.show(self.df)
        self.status.set(f"Reset: {len(self.df)} rows")


if __name__ == "__main__":
    FIIncViewer().mainloop()