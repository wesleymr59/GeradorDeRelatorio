# tests/test_application.py

import pytest
from unittest.mock import Mock
from loguru import logger

from src.application.app import Application


@pytest.fixture
def mock_input():
    mock = Mock()
    # Simula get_arguments retornando um Namespace
    mock.get_arguments.return_value = Mock(
        input_file="mock_file.csv",
        format="json",
        dateStart=None,
        dateEnd=None
    )
    return mock

@pytest.fixture
def mock_output():
    mock = Mock()
    # Simula read_output retornando um relatório de teste
    mock.read_output.return_value = "mock_report"
    return mock

@pytest.fixture
def app(mock_input, mock_output):
    return Application(input_handler=mock_input, output_handler=mock_output)

def test_start_calls_handlers(app, mock_input, mock_output, caplog, capsys):
    log_messages = []
    logger.remove()
    logger.add(log_messages.append, level="INFO")

    app.start()

    mock_input.get_arguments.assert_called_once()
    mock_output.read_output.assert_called_once_with(args=mock_input.get_arguments.return_value)

    captured = capsys.readouterr()
    assert "mock_report" in captured.out

    assert any("Processando arquivo: mock_file.csv" in m for m in log_messages)
    assert any("Formato de saída: json" in m for m in log_messages)

def test_start_handles_exception(app, mock_input, mock_output, caplog):
    # Força uma exceção no output_handler
    mock_output.read_output.side_effect = Exception("fail")
    app = Application(input_handler=mock_input, output_handler=mock_output)

    # Captura logs em lista
    log_messages = []
    logger.remove()  # remove handlers padrão
    logger.add(log_messages.append, level="ERROR")

    app.start()

    # Valida que o erro foi logado
    assert any("Erro ao iniciar a aplicação: fail" in m for m in log_messages)
