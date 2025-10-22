from loguru import logger
from src.infra.input.input import Input
from src.infra.output.output import Output



class Application:
    def __init__(self, input_handler: Input, output_handler: Output):
        self.input_handler = input_handler
        self.output_handler = output_handler

    def start(self):
        try:
            args = self._get_arguments()
            logger.info(f"Processando arquivo: {args.input_file}")
            
            report = self._generate_report(args)
            self._display_report(report)
            
            logger.info(f"Formato de saída: {args.format}")
        except Exception as e:
            logger.error(f"Erro ao iniciar a aplicação: {e}")

    def _get_arguments(self):
        return self.input_handler.get_arguments()

    def _generate_report(self, args):
        return self.output_handler.read_output(args=args)

    def _display_report(self, report: str):
        print(report)
