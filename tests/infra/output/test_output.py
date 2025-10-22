import pytest
from datetime import datetime
from src.infra.output.output import Output
from src.domain.models.models import Products
import argparse
import json

@pytest.fixture
def output():
    return Output()


@pytest.fixture
def mock_args():
    return argparse.Namespace(
        input_file="mock_file.csv",
        dateStart="2023-01-01",
        dateEnd="2023-12-31",
        format="json"
    )


def test_read_output(output):

    args = argparse.Namespace(
        input_file="vendas_exemplo.csv",
        dateStart=None,
        dateEnd=None,
        format="json"
    )

    result = output.read_output(args)

    assert result is not None

def test_convert_to_json(output):
    data = [
        ["produto", "quantidade", "preco_unitario", "data"],
        ["A", "10", "5.0", "2023-01-01"],
        ["B", "20", "3.0", "2023-02-01"]
    ]
    result = output._convert_to_json(data)
    
    assert result[0].produto == "A"
    assert result[1].quantidade == 20


def test_filter_data_by_date(output):
    data = [
        Products(produto="A", quantidade=10, preco_unitario=5.0, data=datetime(2023, 1, 1)),
        Products(produto="B", quantidade=20, preco_unitario=3.0, data=datetime(2023, 2, 1)),
        Products(produto="C", quantidade=15, preco_unitario=2.0, data=datetime(2022, 12, 31))
    ]
    dt_start = datetime(2023, 1, 1).date()
    dt_end = datetime(2023, 12, 31).date()
    result = output._filter_data_by_date(data, dt_start, dt_end)
    
    assert result[0].produto == "A"
    assert result[1].produto == "B"


def test_calculate_totals(output):
    data = [
        Products(produto="A", quantidade=10, preco_unitario=5.0, data=datetime(2023, 1, 1)),
        Products(produto="B", quantidade=20, preco_unitario=3.0, data=datetime(2023, 2, 1)),
        Products(produto="A", quantidade=5, preco_unitario=5.0, data=datetime(2023, 3, 1))
    ]
    total_per_product, total_per_product_quantity, total_overall = output._calculate_totals(data)
    
    assert total_per_product["A"] == 75.0
    assert total_per_product["B"] == 60.0
    assert total_per_product_quantity["A"] == 15
    assert total_per_product_quantity["B"] == 20
    assert total_overall == 135.0


def test_find_best_selling_product(output):
    total_per_product_quantity = {"A": 15, "B": 20}
    best_product, best_quantity = output._find_best_selling_product(total_per_product_quantity)

    assert best_product == "B"
    assert best_quantity == 20


def test_generate_json_output(output):
    total_per_product = {"A": 75.0, "B": 60.0}
    total_overall = 135.0
    most_sold_product = "B"
    most_sold_quantity = 20
    result = output._generate_json_output(total_per_product, total_overall, most_sold_product, most_sold_quantity)
    result_dict = json.loads(result)

    assert result_dict["produtos"]["A"] == 75.0
    assert result_dict["total_geral"] == 135.0
    assert result_dict["mais_vendido"]["produto"] == "B"
    assert result_dict["mais_vendido"]["quantidade"] == 20


def test_generate_text_output(output):
    total_per_product = {"A": 75.0, "B": 60.0}
    total_overall = 135.0
    most_sold_product = "B"
    most_sold_quantity = 20
    result = output._generate_text_output(total_per_product, total_overall, most_sold_product, most_sold_quantity)


    assert "A               |   75.00" in result
    assert "B               |   60.00" in result
    assert "Total Geral   | $ 135.00" in result
    assert "Mais Vendido       | B (20)" in result

def test_calculate_total_sell_products(output, mock_args):
    data = [
        Products(produto="A", quantidade=10, preco_unitario=5.0, data=datetime(2023, 1, 1)),
        Products(produto="B", quantidade=20, preco_unitario=3.0, data=datetime(2023, 2, 1)),
        Products(produto="A", quantidade=5, preco_unitario=5.0, data=datetime(2023, 3, 1))
    ]
    
    total_per_product, total_overall, most_sold_product, most_sold_quantity = output._calculate_total_sell_products(data, mock_args)

    assert total_per_product == {'A': 75.0, 'B': 60.0}
    assert total_overall == 135.0
    assert most_sold_product == 'B'
    assert most_sold_quantity == 20