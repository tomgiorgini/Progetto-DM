"""Build an analysis-ready UFC fight table from three public CSV snapshots."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd


DEFAULT_START_DATE = "2010-03-21"
DEFAULT_END_DATE = "2021-03-20"

OUTPUT_COLUMNS = [
    "r_name", "b_name", "event", "date", "month", "year", "gender",
    "city", "state", "country", "referee", "winner", "finish",
    "finishdetails", "finishround", "titlebout", "weightclass",
    "numberofrounds", "emptyarena", "heightdif", "agedif", "reachdif",
    "r_odds", "r_age", "r_age_range", "r_stance", "b_odds", "b_age",
    "b_age_range", "b_stance", "r_avgkd", "r_avgsigstratt",
    "r_avgsigstrlanded", "r_avgtdatt", "r_avgtdlanded", "r_avgsubatt",
    "r_avgctrltime(seconds)", "b_avgkd", "b_avgsigstratt",
    "b_avgsigstrlanded", "b_avgtdatt", "b_avgtdlanded", "b_avgsubatt",
    "b_avgctrltime(seconds)", "r_undefeated", "b_undefeated",
    "r_wc_ranked", "r_pfp_ranked", "b_wc_ranked", "b_pfp_ranked",
    "r_champion", "b_champion",
]


def normalize_column(name: str) -> str:
    """Normalize source-specific red/blue prefixes and punctuation."""
    name = name.replace("Blue", "B_", 1) if name.startswith("Blue") else name
    name = name.replace("Red", "R_", 1) if name.startswith("Red") else name
    if name.startswith(("R", "B")) and name not in {
        "ReachDif",
        "BetterRank",
        "Referee",
    }:
        if len(name) > 1 and name[1] != "_":
            name = f"{name[0]}_{name[1:]}"
    name = name.lower()
    if name.startswith(("r_", "b_")):
        return name[:2] + name[2:].replace("_", "")
    return name.replace("_", "")


def add_age_group(frame: pd.DataFrame, age_column: str, output_column: str) -> None:
    age = pd.to_numeric(frame[age_column], errors="coerce")
    lower = ((age - 1) // 5) * 5 + 1
    upper = lower + 4
    frame[output_column] = np.where(
        age.notna(),
        lower.astype("Int64").astype(str) + "-" + upper.astype("Int64").astype(str),
        pd.NA,
    )


def _split_location(frame: pd.DataFrame) -> pd.DataFrame:
    parts = frame["location"].astype("string").str.split(",", n=2, expand=True)
    parts = parts.reindex(columns=range(3))
    parts.columns = ["city", "state", "country"]
    parts = parts.apply(lambda column: column.str.strip())
    two_part = parts["country"].isna() & parts["state"].notna()
    parts.loc[two_part, "country"] = parts.loc[two_part, "state"]
    parts.loc[two_part, "state"] = ""
    return frame.drop(columns=["city", "state", "country"], errors="ignore").join(parts)


def _prepare_common(
    frame: pd.DataFrame, start_date: str, end_date: str
) -> pd.DataFrame:
    frame = frame.copy()
    frame.columns = [normalize_column(column) for column in frame.columns]
    frame["date"] = pd.to_datetime(frame["date"], errors="coerce")
    frame = frame.sort_values(["date", "r_fighter"]).reset_index(drop=True)
    frame["month"] = frame["date"].dt.month
    frame["year"] = frame["date"].dt.year
    frame = _split_location(frame)
    frame = frame.loc[frame["date"].between(start_date, end_date)].copy()
    return frame


def prepare_betting_source(
    frame: pd.DataFrame, start_date: str, end_date: str
) -> pd.DataFrame:
    frame = _prepare_common(frame, start_date, end_date)
    frame["r_undefeated"] = pd.to_numeric(frame["r_losses"], errors="coerce").fillna(0).eq(0)
    frame["b_undefeated"] = pd.to_numeric(frame["b_losses"], errors="coerce").fillna(0).eq(0)
    add_age_group(frame, "r_age", "r_age_range")
    add_age_group(frame, "b_age", "b_age_range")
    frame["heightdif"] = (frame["r_heightcms"] - frame["b_heightcms"]).round(2)
    frame["reachdif"] = (frame["r_reachcms"] - frame["b_reachcms"]).round(2)
    frame["agedif"] = (frame["r_age"] - frame["b_age"]).round(2)

    for corner in ("r", "b"):
        frame[f"{corner}_wc_ranked"] = frame[f"{corner}_matchwcrank"].notna()
        frame[f"{corner}_pfp_ranked"] = frame[f"{corner}_pfprank"].notna()
        frame[f"{corner}_champion"] = frame[f"{corner}_matchwcrank"].eq(0).fillna(False)

    columns = [
        "r_fighter", "b_fighter", "date", "month", "year", "gender", "city",
        "state", "country", "finish", "finishdetails", "finishround",
        "titlebout", "weightclass", "numberofrounds", "emptyarena", "r_odds",
        "r_age", "r_age_range", "r_stance", "b_odds", "b_age", "b_age_range",
        "b_stance", "r_wc_ranked", "r_pfp_ranked", "b_wc_ranked",
        "b_pfp_ranked", "r_champion", "b_champion", "r_undefeated",
        "b_undefeated", "heightdif", "reachdif", "agedif",
    ]
    return frame[columns]


def prepare_statistics_source(
    frame: pd.DataFrame, start_date: str, end_date: str
) -> pd.DataFrame:
    frame = _prepare_common(frame, start_date, end_date)
    columns = [
        "r_fighter", "b_fighter", "date", "referee", "winner", "r_avgkd",
        "r_avgsigstratt", "r_avgsigstrlanded", "r_avgtdatt", "r_avgtdlanded",
        "r_avgsubatt", "r_avgctrltime(seconds)", "b_avgkd", "b_avgsigstratt",
        "b_avgsigstrlanded", "b_avgtdatt", "b_avgtdlanded", "b_avgsubatt",
        "b_avgctrltime(seconds)",
    ]
    return frame[columns]


def _find_swapped_rows(left: pd.DataFrame, right: pd.DataFrame) -> list[int]:
    left_keys = left[["date", "r_fighter", "b_fighter"]].drop_duplicates()
    swapped = right.reset_index(names="row").merge(
        left_keys,
        left_on=["date", "r_fighter", "b_fighter"],
        right_on=["date", "b_fighter", "r_fighter"],
        how="inner",
        suffixes=("_right", "_left"),
    )
    return sorted(swapped["row"].astype(int).unique().tolist())


def _swap_corners(frame: pd.DataFrame, rows: list[int]) -> pd.DataFrame:
    frame = frame.copy()
    pairs = [
        (column, "b_" + column[2:])
        for column in frame.columns
        if column.startswith("r_") and "b_" + column[2:] in frame.columns
    ]
    for red, blue in pairs:
        red_values = frame.loc[rows, red].copy()
        frame.loc[rows, red] = frame.loc[rows, blue].to_numpy()
        frame.loc[rows, blue] = red_values.to_numpy()
    winner = frame.loc[rows, "winner"].astype("string").str.strip()
    frame.loc[rows, "winner"] = winner.str.lower().map(
        {"blue": "Red", "red": "Blue"}
    ).fillna(winner)
    return frame


def _align_fighter_names(left: pd.DataFrame, right: pd.DataFrame) -> tuple[pd.DataFrame, int]:
    """Use the betting-source spelling when one fighter and date already match."""
    right = right.copy()
    changed_rows: set[int] = set()
    left_indexed = left.reset_index(names="left_row")
    right_indexed = right.reset_index(names="right_row")

    same_red = left_indexed.merge(
        right_indexed, on=["date", "r_fighter"], suffixes=("_left", "_right")
    )
    same_red = same_red[same_red["b_fighter_left"] != same_red["b_fighter_right"]]
    for row in same_red.itertuples():
        right.loc[row.right_row, "b_fighter"] = row.b_fighter_left
        changed_rows.add(int(row.right_row))

    same_blue = left_indexed.merge(
        right.reset_index(names="right_row"),
        on=["date", "b_fighter"],
        suffixes=("_left", "_right"),
    )
    same_blue = same_blue[same_blue["r_fighter_left"] != same_blue["r_fighter_right"]]
    for row in same_blue.itertuples():
        right.loc[row.right_row, "r_fighter"] = row.r_fighter_left
        changed_rows.add(int(row.right_row))
    return right, len(changed_rows)


def integrate_sources(
    betting: pd.DataFrame, statistics: pd.DataFrame, events: pd.DataFrame
) -> tuple[pd.DataFrame, dict[str, int]]:
    swapped_rows = _find_swapped_rows(betting, statistics)
    statistics = _swap_corners(statistics, swapped_rows)
    statistics, renamed_rows = _align_fighter_names(betting, statistics)

    betting = betting.rename(columns={"r_fighter": "r_name", "b_fighter": "b_name"})
    statistics = statistics.rename(columns={"r_fighter": "r_name", "b_fighter": "b_name"})
    fights = betting.merge(statistics, on=["r_name", "b_name", "date"], how="outer")

    events = events.copy()
    events.columns = [normalize_column(column) for column in events.columns]
    events["date"] = pd.to_datetime(events["date"], errors="coerce")
    fights = fights.merge(events[["date", "event"]], on="date", how="left")
    fights = fights.dropna(subset=["winner", "city"]).copy()

    average_columns = [column for column in fights if column.startswith(("r_avg", "b_avg"))]
    fights[average_columns] = fights[average_columns].fillna(0)
    integer_columns = [
        "month", "year", "finishround", "numberofrounds", "r_odds", "b_odds",
        "r_age", "b_age", "agedif",
    ]
    for column in integer_columns:
        fights[column] = pd.to_numeric(fights[column], errors="coerce").astype("Int64")
    boolean_columns = [
        "titlebout", "emptyarena", "r_undefeated", "b_undefeated",
        "r_wc_ranked", "r_pfp_ranked", "b_wc_ranked", "b_pfp_ranked",
        "r_champion", "b_champion",
    ]
    fights[boolean_columns] = fights[boolean_columns].astype(bool)
    fights = fights[OUTPUT_COLUMNS].sort_values(["date", "r_name"]).reset_index(drop=True)
    if fights.columns.duplicated().any() or fights.duplicated().any():
        raise ValueError("ETL produced duplicate columns or rows")
    return fights, {"swapped_corner_rows": len(swapped_rows), "aligned_name_rows": renamed_rows}


def run_etl(
    input_dir: Path,
    output_dir: Path,
    start_date: str = DEFAULT_START_DATE,
    end_date: str = DEFAULT_END_DATE,
    write_intermediates: bool = False,
) -> tuple[pd.DataFrame, dict[str, Any]]:
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    raw_betting = pd.read_csv(input_dir / "d1.csv")
    raw_statistics = pd.read_csv(input_dir / "d2.csv")
    raw_events = pd.read_csv(input_dir / "d3.csv")
    betting = prepare_betting_source(raw_betting, start_date, end_date)
    statistics = prepare_statistics_source(raw_statistics, start_date, end_date)
    fights, corrections = integrate_sources(betting, statistics, raw_events)

    output_file = output_dir / "fights.csv"
    fights.to_csv(output_file, index=False, date_format="%Y-%m-%d")
    if write_intermediates:
        betting.to_csv(output_dir / "betting_clean.csv", index=False, date_format="%Y-%m-%d")
        statistics.to_csv(output_dir / "statistics_clean.csv", index=False, date_format="%Y-%m-%d")

    report: dict[str, Any] = {
        "source_rows": {
            "betting": len(raw_betting),
            "statistics": len(raw_statistics),
            "events": len(raw_events),
        },
        "output_rows": len(fights),
        "output_columns": len(fights.columns),
        "date_range": [fights["date"].min().date().isoformat(), fights["date"].max().date().isoformat()],
        **corrections,
    }
    (output_dir / "etl_report.json").write_text(json.dumps(report, indent=2) + "\n")
    return fights, report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", type=Path, default=Path("data/raw"))
    parser.add_argument("--output-dir", type=Path, default=Path("data/processed"))
    parser.add_argument("--start-date", default=DEFAULT_START_DATE)
    parser.add_argument("--end-date", default=DEFAULT_END_DATE)
    parser.add_argument("--write-intermediates", action="store_true")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    _, report = run_etl(
        args.input_dir,
        args.output_dir,
        args.start_date,
        args.end_date,
        args.write_intermediates,
    )
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
