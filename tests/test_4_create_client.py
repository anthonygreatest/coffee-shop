import json
from http import HTTPStatus

import allure

from utils.schemas.token_resp_schema import TokenValidationSchema

@allure.story('Registering Customer')
def test_register_client(assertion, token_from_client, validation):

    with allure.step('Checking Customer Registered'):
        headers, resp = token_from_client

        validation.validate_response(
            response=resp,
            schema=TokenValidationSchema
        )

        assertion.assert_response_status_code(
            response=resp,
            expected=HTTPStatus.OK
        )

        allure.attach(
            json.dumps(resp.json(), indent=2),
            name='Registration Token',
            attachment_type=allure.attachment_type.JSON
        )


