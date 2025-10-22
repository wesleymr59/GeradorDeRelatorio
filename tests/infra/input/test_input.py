import sys
import pytest

from src.infra.input.input import Input


@pytest.fixture
def input_cli():
    return Input()

def test_parse_arguments_json(input_cli, monkeypatch):
    """Testa parsing com formato JSON e datas válidas"""
    test_args = [
        "prog",
        "vendas_exemplo.csv",
        "--format", "json",
        "--dateStart", "2025-01-01",
        "--dateEnd", "2025-01-02"
    ]
    monkeypatch.setattr(sys, "argv", test_args)

    args = input_cli.get_arguments()

    assert args.input_file == "vendas_exemplo.csv"
    assert args.format == "json"
    assert args.dateStart == "2025-01-01"
    assert args.dateEnd == "2025-01-02"


def test_parse_arguments_text_default(input_cli, monkeypatch):
    test_args = ["prog", "vendas_exemplo.csv"]
    monkeypatch.setattr(sys, "argv", test_args)

    args = input_cli.get_arguments()

    assert args.input_file == "vendas_exemplo.csv"
    assert args.format == "json"
    assert args.dateStart is None
    assert args.dateEnd is None


def test_missing_input_file(input_cli, monkeypatch):
    test_args = ["prog"]
    monkeypatch.setattr(sys, "argv", test_args)

    with pytest.raises(SystemExit):
        input_cli.get_arguments()
