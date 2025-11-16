

class Assertions:

    def assert_response_status_code(self, response, expected):

        if isinstance(response, list):
            for item in response:
                assert item == expected, \
                f'Wrong status code, expected {expected}, got {item}'
        else:
            assert response.status_code == expected,\
            f'Wrong status code, expected {expected}, got {response.status_code}'

    def assert_products_length(self, response, params):

        assert len(response.json()['products']) == params.limit

    def assert_products_categories(self, response, params):

        for item in response.json()['products']:
            assert item['category'] == params.category

    def assert_response_matches_request(self, response, request):

        assert response.json()['id'] == request, \
            f'Wrong response, expected {request}, got {response.json()['id']}'

    def assert_orders_response(self, response, request):

        if isinstance(response, list):
            for i in range(len(response)):
                assert response[i]['customerName'] == request[i]['customerName']

                assert (sorted(response[i]['products'], key=lambda x: x['id']) ==
                        sorted(request[i]['products'], key=lambda x: x['id']))
        else:
            assert response.json()['customerName'] == request['customerName']

            assert (sorted(response.json()['products'], key=lambda x: x['id']) ==
                    sorted(request['products'], key=lambda x: x['id']))