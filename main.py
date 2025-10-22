from src.application.app import Application
from src.infra.input.input import Input
from src.infra.output.output import Output



def main():
    input_handler = Input()
    output_handler = Output()
    app = Application(input_handler=input_handler, output_handler=output_handler)
    app.start()


if __name__ == "__main__":
    main()