import json

import allure

from utils.schemas.single_product_schema import SingleProductSchema

@allure.story('Getting all products')
def test_get_single_product(assertion, validation, get_one_product):

    with allure.step('Check getting single product'):
        resp, request_id = get_one_product

        assertion.assert_response_matches_request(
            response=resp,
            request=request_id['id']
        )

        validation.validate_response(
            response=resp,
            schema=SingleProductSchema
        )

        allure.attach(
            json.dumps(resp.json(), indent=2),
            name='One Product Selected',
            attachment_type=allure.attachment_type.JSON
        )
