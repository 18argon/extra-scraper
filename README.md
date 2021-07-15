# Extra Scraper

Web Scraper de ofertas para produtos vendidos no site https://www.extra.com.br.

A ferramenta efetua a extração dos produtos nas categorias Impressora, Televisores, e Refrigeradores.

O número de páginas a serem percorridas pode ser ajustado no arquivo `extra_scraper/extra_scraper/settings.py`, alterando as variáveis `MAX_PRODUCTS_PAGE` e `MAX_PRODUCTS_PAGE`. Essa limitação pode ser removida ao atribuir o valor -1 a uma ou ambas as variáveis.

## Dependências
As dependências podem ser instaladas com o auxilio da ferramenta [pip](https://pip.pypa.io/en/stable/) ao executar o comando `pip install -r requirements.txt` na pasta root do repositório.

## Execução
A ferramenta é executada com o comando `scrapy crawl products` na pasta `extra-scraper`.

## Exemplos
Na pasta `examples` estão disponíveis exemplos de saída para avaliações e produtos para as 3 categorias.

Foram obtidos todas as avaliações para a primeira página de cada categoria.

Os dados foram obtidos em 15/07/2021, às 03:38.
