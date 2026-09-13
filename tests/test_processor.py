import pandas as pd

from src.processor import DataProcessor, clean_data


def test_clean_data_trims_strings_and_drops_duplicates():
    dirty = pd.DataFrame(
        [
            {"State": " Lagos ", "LGA": " Ikeja ", "Ward": " Ward A "},
            {"State": "Lagos", "LGA": "Ikeja", "Ward": "Ward A"},
        ]
    )

    cleaned = clean_data(dirty)

    assert len(cleaned) == 1
    assert cleaned.iloc[0].to_dict() == {
        "State": "Lagos",
        "LGA": "Ikeja",
        "Ward": "Ward A",
    }


def test_process_to_csv_writes_hierarchical_exports(tmp_path):
    processor = DataProcessor(output_dir=tmp_path)

    result = processor.process_to_csv(
        wards_data=[
            ("Lagos", "Ikeja", "Ward A"),
            ("Lagos", "Ikeja", "Ward A"),
            ("Lagos", "Eti-Osa", "Ward B"),
        ],
        pus_data=[
            ("Lagos", "Ikeja", "Ward A", "PU 001"),
            ("Lagos", "Eti-Osa", "Ward B", "PU 002"),
        ],
    )

    assert list(result.columns) == ["State", "LGA", "Ward", "Polling Unit"]
    assert (tmp_path / "All_LGAs.csv").exists()
    assert (tmp_path / "All_LGA_Wards.csv").exists()
    assert (tmp_path / "All_Wards_PUs.csv").exists()

    lgas = pd.read_csv(tmp_path / "All_LGAs.csv")
    assert lgas.to_dict("records") == [
        {"State": "Lagos", "LGA": "Eti-Osa"},
        {"State": "Lagos", "LGA": "Ikeja"},
    ]
