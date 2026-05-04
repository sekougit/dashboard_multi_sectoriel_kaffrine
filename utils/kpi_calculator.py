import numpy as np

def compute_kpis(df):
    kpis = {}

    numeric_cols = df.select_dtypes(include=np.number).columns

    for col in numeric_cols:
        kpis[col] = {
            "total": df[col].sum(),
            "moyenne": df[col].mean()
        }

    return kpis