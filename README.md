
# Gerador de Relatorio

Este projeto fornece uma CLI para gerar relatórios de vendas a partir de arquivos CSV, permitindo filtragem por datas e exportação em diferentes formatos.

## Pré-requisitos

- Python 3.13+
- Poetry (opcional, para gerenciamento de dependências)
- Make (ou GNU Make, para Windows use PowerShell ou WSL)

## Instalação

Instale as dependências usando Poetry:

```bash
poetry install
pip install -e .

Se você estiver usando o Makefile, basta rodar:

make install_project
```

## Executando o Projeto

Uso da CLI
```bash
vendas-cli <caminho_do_arquivo> [--format {json,text}] [--start YYYY-MM-DD] [--end YYYY-MM-DD]
```
Parâmetros

<caminho_do_arquivo>: Caminho para o arquivo CSV de entrada. Obrigatório.

--format ou -f: Formato de saída do relatório. Pode ser json ou text. Padrão: json.

--start ou -ds: Data inicial do filtro (YYYY-MM-DD). Opcional.

--end ou -de: Data final do filtro (YYYY-MM-DD). Opcional.

Se os parâmetros opcionais de data não forem informados, o relatório será gerado para todos os registros disponíveis no CSV.


Exemplos

Relatório JSON para todo o período:

```bash
vendas-cli vendas.csv --format json
```
```bash
vendas-cli vendas.csv --format text
```
```bash
vendas-cli vendas.csv --format json --start 2025-01-01 --end 2025-03-31
```
```bash
vendas-cli vendas.csv --format text --start 2025-01-01 --end 2025-03-31
```

Atalhos via Makefile

| Comando        | Descrição                                               |
| -------------- | ------------------------------------------------------- |
| `make_run`     | Roda a aplicação normalmente.                           |
| `run_text`     | Roda a aplicação e gera o relatório em formato texto.   |
| `run_datetime` | Roda a aplicação usando datas predefinidas no Makefile. |

## Observações

Certifique-se de que o CSV de entrada esteja no formato correto, com as colunas: produto,quantidade,preco_unitario,data.

Campos vazios ou inválidos serão ignorados durante a geração do relatório.
