from src import config


def test_state_inventory_includes_all_regions():
    assert len(config.NIGERIAN_STATES) == 37
    assert "Lagos" in config.NIGERIAN_STATES
    assert "FCT" in config.NIGERIAN_STATES


def test_column_mapping_documents_source_mislabels():
    assert config.COLUMN_MAPPING == {
        "LGA": "State",
        "Ward": "LGA",
        "Polling Unit": "Ward",
    }


def test_next_page_selectors_are_plain_strings():
    assert config.NEXT_PAGE_SELECTORS[0] == "link"
    assert all(isinstance(selector, str) for selector in config.NEXT_PAGE_SELECTORS)
