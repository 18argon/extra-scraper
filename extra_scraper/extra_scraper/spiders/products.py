import json
import scrapy
from urllib import parse

PRODUCTS_PER_PAGE = 20


def get_url(filter_code, page=0, quantityPerPage=PRODUCTS_PER_PAGE):
    return f'https://www.extra.com.br/api/catalogo-ssr/products/?Filtro={filter_code}&PaginaAtual={page}&RegistrosPorPagina={quantityPerPage}&Platform=1'


class ProductsSpider(scrapy.Spider):
    name = 'products'

    start_urls = [
        get_url('c56_c61'),      # Impressoras
        get_url('c1_c2'),        # Televisores
        get_url('c13_c14_C13'),  # Refrigeradores
    ]

    def parse(self, response):
        # Extraindo parâmetros da URL
        query_params = parse.parse_qs(parse.urlsplit(response.url).query)
        query_params = {k.lower(): v for k, v in query_params.items()}
        page = int(query_params['paginaatual'][0])
        filter_code = query_params['filtro'][0]

        jsonresponse = json.loads(response.text)
        # Total de item na catergoria
        total = jsonresponse['size']

        for product in jsonresponse['products']:
            yield {
                'productId': product['id'],
                'filter_code': filter_code.lower(),
                'url': product['urls'],
                'title': product['name'],
                'skuId': product['urls'].split('/')[-1]
            }

        # Paginação
        if (page + 1) * PRODUCTS_PER_PAGE < total and page < 0:
            url = get_url(filter_code, page + 1)

            yield scrapy.Request(url=url, callback=self.parse)
