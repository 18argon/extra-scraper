import json
from urllib import parse
import scrapy
from extra_scraper.items import ReviewItem, ProductItem
from scrapy.utils.project import get_project_settings

settings = get_project_settings()

PRODUCTS_PER_PAGE = 20
REVIEWS_PER_PAGE = 3

MAX_PRODUCTS_PAGE = settings['MAX_PRODUCTS_PAGE']
MAX_REVIEW_PAGE = settings['MAX_REVIEW_PAGE']


def get_products_url(filter_code, page=0, quantityPerPage=PRODUCTS_PER_PAGE):
    return f'https://www.extra.com.br/api/catalogo-ssr/products/?Filtro={filter_code}&PaginaAtual={page}&RegistrosPorPagina={quantityPerPage}&Platform=1'


def get_reviews_url(productId, page=0, quantityPerPage=REVIEWS_PER_PAGE):
    return f'https://pdp-api.extra.com.br/api/v2/reviews/product/{productId}/source/EX?page={page}&size={quantityPerPage}&orderBy=DATE'


class ProductsSpider(scrapy.Spider):
    name = 'products'

    start_urls = [
        get_products_url('c56_c61'),      # Impressoras
        get_products_url('c1_c2'),        # Televisores
        get_products_url('c13_c14_C13'),  # Refrigeradores
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
            yield ProductItem(
                productId=product['id'],
                filter_code=filter_code.lower(),
                url=product['urls'],
                title=product['name'],
                skuId=product['urls'].split('/')[-1]
            )

        yield scrapy.Request(url=get_reviews_url(product['id']), callback=self.parse_reviews)

        # Paginação
        if (page + 1) * PRODUCTS_PER_PAGE < total:
            if MAX_PRODUCTS_PAGE == -1 or (page + 1) < MAX_PRODUCTS_PAGE:
                yield scrapy.Request(url=get_products_url(filter_code, page + 1), callback=self.parse)

    def parse_reviews(self, response):
        url_split = parse.urlsplit(response.url)
        query_params = parse.parse_qs(url_split.query)
        query_params = {k.lower(): v for k, v in query_params.items()}
        page = int(query_params['page'][0])
        productId = int(url_split.path.split('/')[-3])

        json_response = json.loads(response.text)

        review = json_response['review']
        for user_review in review['userReviews']:
            yield ReviewItem(
                productId=productId,
                reviewId=user_review['id'],
                text=user_review['text'],
                date=user_review['date'],
                dislikes=user_review['dislikes'],
                likes=user_review['likes'],
            )

        if ((page + 1) * REVIEWS_PER_PAGE < review['ratingQty'] or not review['lastPage']):
            if MAX_REVIEW_PAGE == -1 or (page + 1) < MAX_REVIEW_PAGE:
                yield scrapy.Request(url=get_reviews_url(productId, page+1), callback=self.parse_reviews)
