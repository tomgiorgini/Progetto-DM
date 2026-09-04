from pathlib import Path

import pandas as pd

from ufc_dw.etl import OUTPUT_COLUMNS, add_age_group, run_etl


ROOT = Path(__file__).resolve().parents[1]


def test_age_groups_handle_boundaries_and_missing_values() -> None:
    frame = pd.DataFrame({"age": [20, 21, 25, 26, None]})
    add_age_group(frame, "age", "age_range")
    assert frame["age_range"].tolist()[:4] == ["16-20", "21-25", "21-25", "26-30"]
    assert pd.isna(frame.loc[4, "age_range"])


def test_full_etl_contract(tmp_path: Path) -> None:
    fights, report = run_etl(ROOT / "data/raw", tmp_path)

    assert list(fights.columns) == OUTPUT_COLUMNS
    assert fights.columns.is_unique
    assert not fights.duplicated().any()
    assert fights["winner"].notna().all()
    assert fights["city"].notna().all()
    assert report["output_rows"] == len(fights)
    assert report["output_columns"] == len(OUTPUT_COLUMNS)
    assert (tmp_path / "fights.csv").is_file()
    assert (tmp_path / "etl_report.json").is_file()
