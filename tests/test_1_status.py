import allure

from utils.schemas.status_resp_schema import StatusResponseSchema
from .conftest import validation
from http import HTTPStatus

@allure.story('Test status')
def test_status(api_client, assertion, validation):

    with allure.step('Check getting test status'):
        resp = api_client.get_status()

        validation.validate_response(
            response=resp,
            schema=StatusResponseSchema
        )

        assertion.assert_response_status_code(
            response=resp,
            expected=HTTPStatus.OK
        )

        assert resp.json()['status'] == "API is up and running"

