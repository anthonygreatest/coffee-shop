import json
from http import HTTPStatus

import allure
from sqlalchemy import desc

from utils.schemas.token_resp_schema import TokenValidationSchema
from utils.tables import Clients


@allure.story('Registering Customer')
def test_register_client(assertion, token_from_client, validation):

    with allure.step('Checking Customer Registered'):
        headers, resp, _ = token_from_client

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

def test_client_added_to_db(get_db_session, token_from_client):

        _, _, clients_to_db = token_from_client

        data_from_db = get_db_session.query(Clients.email, Clients.token).order_by(desc(Clients.created_at)).first()

        assert data_from_db[0] == clients_to_db['email']



