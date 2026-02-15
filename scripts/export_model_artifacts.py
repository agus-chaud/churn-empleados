"""
Genera artifacts/modeling/best_model.pkl y preprocessor.pkl para que el dashboard
muestre el gráfico de importancia de variables.

Ejecutar desde la raíz del proyecto:
  python scripts/export_model_artifacts.py

Requisitos: AbandonoEmpleados.csv en la raíz (o ruta indicada con --csv).
Si ya tiene pipeline/preprocessor desde el notebook, no es necesario ejecutar esto.
"""
import argparse
import json
import sys
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline as ImbPipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from xgboost import XGBClassifier

ROOT = Path(__file__).resolve().parent.parent
ARTIFACTS = ROOT / "artifacts" / "modeling"
MANIFEST_PATH = ARTIFACTS / "experiment_manifest.json"


def main():
    parser = argparse.ArgumentParser(description="Exportar pipeline y preprocessor para el dashboard")
    parser.add_argument("--csv", default=None, help="Ruta al CSV (default: AbandonoEmpleados.csv en la raíz)")
    args = parser.parse_args()
    csv_path = Path(args.csv) if args.csv else ROOT / "AbandonoEmpleados.csv"
    if not csv_path.exists():
        print(f"No se encontró {csv_path}. Indique --csv o coloque AbandonoEmpleados.csv en la raíz.", file=sys.stderr)
        sys.exit(1)

    # Cargar manifest para feature_columns
    feature_columns = []
    if MANIFEST_PATH.exists():
        with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
            manifest = json.load(f)
            feature_columns = manifest.get("feature_columns", [])

    df = pd.read_csv(csv_path, sep=";", index_col="id", na_values="#N/D")
    if "abandono" not in df.columns:
        print("El CSV no tiene columna 'abandono'.", file=sys.stderr)
        sys.exit(1)
    y = df["abandono"].replace({"Yes": 1, "No": 0}).astype(int)
    available = [c for c in feature_columns if c in df.columns] if feature_columns else df.columns.drop("abandono").tolist()
    available = [c for c in available if c != "abandono"]
    if not available:
        available = [c for c in df.select_dtypes(include=[np.number]).columns if c not in ("abandono", "impacto_abandono", "scoring_abandono")]
        available += [c for c in df.select_dtypes(include=["object"]).columns if c != "abandono"]
    X = df[available].copy()
    X = X.dropna(axis=1, how="all")
    available = list(X.columns)
    num_cols = [c for c in available if X[c].dtype in (np.int64, np.float64)]
    cat_cols = [c for c in available if c not in num_cols]
    if not num_cols and not cat_cols:
        print("No quedan columnas útiles para entrenar.", file=sys.stderr)
        sys.exit(1)

    X = X[num_cols + cat_cols]
    train_x, test_x, train_y, test_y = train_test_split(X, y, test_size=0.3, random_state=42)

    preprocessor = ColumnTransformer([
        ("num", Pipeline([
            ("impute", SimpleImputer(strategy="median")),
            ("scale", StandardScaler()),
        ]), num_cols),
        ("cat", OneHotEncoder(sparse_output=False, handle_unknown="ignore"), cat_cols),
    ])
    preprocessor.fit(train_x)
    train_x_t = preprocessor.transform(train_x)
    test_x_t = preprocessor.transform(test_x)

    scale_pos_weight = (train_y == 0).sum() / max((train_y == 1).sum(), 1)
    pipeline = ImbPipeline([
        ("smote", SMOTE(random_state=42, k_neighbors=3, sampling_strategy=0.6)),
        ("clf", XGBClassifier(
            scale_pos_weight=scale_pos_weight,
            random_state=42,
            use_label_encoder=False,
            eval_metric="logloss",
            n_estimators=50,
            max_depth=5,
            learning_rate=0.1,
        )),
    ])
    pipeline.fit(train_x_t, train_y)

    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipeline, ARTIFACTS / "best_model.pkl")
    joblib.dump(preprocessor, ARTIFACTS / "preprocessor.pkl")
    print(f"Guardado: {ARTIFACTS / 'best_model.pkl'}, {ARTIFACTS / 'preprocessor.pkl'}")
    print("Reinicie el dashboard para ver el gráfico de importancia de variables.")

    # Opcional: guardar feature_importances en el manifest para no depender del .pkl
    clf = pipeline.steps[-1][1]
    if hasattr(clf, "feature_importances_"):
        names = preprocessor.get_feature_names_out()
        imp = clf.feature_importances_
        imp_list = [{"variable": names[i], "importancia": float(imp[i])} for i in range(len(imp))]
        if MANIFEST_PATH.exists():
            with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
                m = json.load(f)
            if "best_model" not in m:
                m["best_model"] = {}
            m["best_model"]["feature_importances"] = imp_list
            with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
                json.dump(m, f, indent=2, ensure_ascii=False)
            print("Manifest actualizado con feature_importances.")


if __name__ == "__main__":
    main()
