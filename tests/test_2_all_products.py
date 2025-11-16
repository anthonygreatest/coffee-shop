import json

import allure

from utils.schemas.all_products_schema import AllProductResponseSchema

@allure.story('Getting all products')
def test_all_products(assertion, validation, all_products):
    with allure.step('Check getting all products'):
        resp, params = all_products

        assertion.assert_products_categories(
            response=resp,
            params=params
        )

        validation.validate_response(
            response=resp.json()['products'],
            schema=AllProductResponseSchema
        )
        allure.attach(
            json.dumps(resp.json(), indent=2),
            name='Selected Products',
            attachment_type=allure.attachment_type.JSON
        )

@allure.story('Getting all products')
def test_products_length(assertion, validation, all_products):
    with allure.step('Check length of all products'):
        resp, params = all_products

        assertion.assert_products_length(
            response=resp,
            params=params
        )
