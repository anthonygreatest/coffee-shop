

from utils.schemas.all_products_schema import AllProductResponseSchema


def test_all_products(assertion, validation, all_products):

    resp, params = all_products

    assertion.assert_products_categories(
        response=resp,
        params=params
    )

    validation.validate_response(
        response=resp.json()['products'],
        schema=AllProductResponseSchema
    )

def test_products_length(assertion, validation, all_products):

    resp, params = all_products

    assertion.assert_products_length(
        response=resp,
        params=params
    )
