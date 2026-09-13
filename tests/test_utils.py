from src import utils


class DummyResponse:
    text = """
    <html>
      <body>
        <table>
          <tr><th>LGA</th><th>Ward</th><th>Polling Unit</th></tr>
          <tr><td>Lagos</td><td>Ikeja</td><td>Ward A</td></tr>
          <tr><td>Oyo</td><td>Ibadan North</td><td>Ward B</td></tr>
        </table>
      </body>
    </html>
    """


def test_legacy_scrape_filters_rows_using_config_mapping(monkeypatch):
    monkeypatch.setattr(utils.requests, "get", lambda url: DummyResponse())

    result = utils.legacy_scrape(
        url="https://example.test/table",
        focus_level="State",
        state_filter="lagos",
    )

    assert result is not None
    assert result.to_dict("records") == [
        {"LGA": "Lagos", "Ward": "Ikeja", "Polling Unit": "Ward A"}
    ]
