from collections import defaultdict
from datetime import datetime
import json
from typing import Dict, List, Tuple
from loguru import logger
import argparse
import sys
import csv

from src.domain.models.models import Products



class Output:

    def read_output(self, args: argparse.Namespace):
        try:
            with open(args.input_file, 'r') as f:
                reader = csv.reader(f)
                data = self._convert_to_json(list(reader))
                return self.principal_calculation(data, args)
        except FileNotFoundError:
            logger.error(f"Arquivo '{args.input_file}' não encontrado!")
            sys.exit(1)
        except Exception as e:
            logger.error(f"Erro ao ler arquivo: {e}")
            sys.exit(1)

    def _convert_to_json(self, data: list) -> List[Products]:
        try:
            headers = data[0]
            rows = data[1:]
            dict_data = [dict(zip(headers, row)) for row in rows]
            products_list = [Products(**item) for item in dict_data]
            return products_list
        except Exception as e:
            logger.error(f"Erro ao converter para JSON: {e}")
            return []

    def principal_calculation(self, data: List[Products], args) -> str:
        dt_start = datetime.strptime(args.dateStart, "%Y-%m-%d").date() if args.dateStart else None
        dt_end = datetime.strptime(args.dateEnd, "%Y-%m-%d").date() if args.dateEnd else None

        filtered_data = self._filter_data_by_date(data, dt_start, dt_end)
        total_per_product, total_per_product_quantity, total_overall = self._calculate_totals(filtered_data)
        most_sold_product, most_sold_quantity = self._find_best_selling_product(total_per_product_quantity)

        return self._hydrate_data_return(args.format, total_per_product, total_overall, most_sold_product, most_sold_quantity)

    def _filter_data_by_date(self, data: List[Products], dt_start: datetime, dt_end: datetime) -> List[Products]:
        return [
            item for item in data
            if item.data and (not dt_start or item.data.date() >= dt_start) and (not dt_end or item.data.date() <= dt_end)
        ]

    def _calculate_totals(self, data: List[Products]) -> Tuple[Dict[str, float], Dict[str, int], float]:
        total_per_product = defaultdict(float)
        total_per_product_quantity = defaultdict(int)
        total_overall = 0

        for item in data:
            subtotal = float(item.quantidade) * float(item.preco_unitario)
            total_per_product[item.produto] += subtotal
            total_per_product_quantity[item.produto] += int(item.quantidade)
            total_overall += subtotal

        return total_per_product, total_per_product_quantity, total_overall

    def _find_best_selling_product(self, total_per_product_quantity: Dict[str, int]) -> Tuple[str, int]:
        if not total_per_product_quantity:
            return None, 0
        best_product = max(total_per_product_quantity, key=total_per_product_quantity.get)
        return best_product, total_per_product_quantity[best_product]

    def _hydrate_data_return(
        self,
        data_type: str,
        total_per_product: Dict[str, float],
        total_overall: float,
        most_sold_product: str,
        most_sold_quantity: int
    ) -> str:
        try:
            match data_type:
                case "json":
                    return self._generate_json_output(total_per_product, total_overall, most_sold_product, most_sold_quantity)
                case "text":
                    return self._generate_text_output(total_per_product, total_overall, most_sold_product, most_sold_quantity)
                case _:
                    raise ValueError(f"Tipo de dado não suportado: {data_type}")
        except Exception as e:
            logger.error(f"Erro ao hidratar dados: {e}")
            return ""

    def _generate_json_output(
        self,
        total_per_product_value: Dict[str, float],
        total_overall: float,
        most_sold_product: str,
        most_sold_quantity: int
    ) -> str:
        output = {
            "produtos": {product: round(value, 2) for product, value in total_per_product_value.items()},
            "total_geral": round(total_overall, 2),
            "mais_vendido": {
                "produto": most_sold_product,
                "quantidade": most_sold_quantity
            }
        }
        return json.dumps(output, indent=4, ensure_ascii=False)

    def _generate_text_output(
        self,
        total_per_product_value: Dict[str, float],
        total_overall: float,
        most_sold_product: str,
        most_sold_quantity: int
    ) -> str:
        lines = ["PRODUTO          | TOTAL"]
        lines.append("----------------|---------")
        for product, value in total_per_product_value.items():
            lines.append(f"{product:<15} | {value:>7.2f}")
        lines.append("----------------|---------")
        lines.append(f"Total Geral   | ${total_overall:>7.2f}")
        lines.append(f"Mais Vendido       | {most_sold_product} ({most_sold_quantity})")
        return "\n".join(lines)

    def _calculate_total_sell_products(self, data: List[Products], args: argparse.Namespace):
        dt_start = datetime.strptime(args.dateStart, "%Y-%m-%d").date() if args.dateStart else None
        dt_end = datetime.strptime(args.dateEnd, "%Y-%m-%d").date() if args.dateEnd else None

        try:
            filtered_data = self._filter_data_by_date(data, dt_start, dt_end)
            total_per_product, total_per_product_quantity, total_overall = self._calculate_totals(filtered_data)
            most_sold_product, most_sold_quantity = self._find_best_selling_product(total_per_product_quantity)

            return total_per_product, total_overall, most_sold_product, most_sold_quantity
        except Exception as e:
            logger.exception(f"Erro inesperado ao calcular total de vendas: {e}")
            return defaultdict(float), 0.0, "", 0
