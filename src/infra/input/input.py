import argparse
import sys
from pathlib import Path

class Input:
    def __init__(self):
        self.parser = self._create_parser()
    
    def _create_parser(self):
        parser = argparse.ArgumentParser(
            description="Gerador de Relatórios",
            formatter_class=argparse.RawDescriptionHelpFormatter
        )
        
        # Argumentos obrigatórios
        parser.add_argument(
            'input_file',
            help='Arquivo de entrada (CSV)'
        )
        # Argumentos obrigatórios
        
        parser.add_argument(
            '-f', '--format',
            choices=['json', 'text'],
            default='json',
            help='Formato do relatório (padrão: json)'
        )
 
        parser.add_argument(
            '-ds', '--dateStart',
            help='Data de início do relatório'
        )
        parser.add_argument(
            '-dse', '--dateEnd',
            help='Data de fim do relatório'
        )
        
        return parser
    
    def parse_arguments(self):
        try:
            args = self.parser.parse_args()
            return args
        except argparse.ArgumentError as e:
            print(f"Erro nos argumentos: {e}")
            sys.exit(1)
        except SystemExit:
            sys.exit(0)
    
    def get_arguments(self):
        return self.parse_arguments()