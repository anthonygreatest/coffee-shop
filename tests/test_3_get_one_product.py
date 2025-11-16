from utils.schemas.single_product_schema import SingleProductSchema


def test_get_single_product(assertion, validation, get_one_product):

    resp, request_id = get_one_product

    assertion.assert_response_matches_request(
        response=resp,
        request=request_id['id']
    )

    validation.validate_response(
        response=resp,
        schema=SingleProductSchema
    )
    print(resp.json())