import pytest

api_version = 'v1/'


def test_product_import(test_client):
    test_csv_file = 'tests/test_products.csv'

    with open(test_csv_file, 'r') as csv_file:
        response = test_client.put('/products/' + api_version, data=csv_file)

        assert 202 == response.status_code
        json_data = response.json
        assert "success" == json_data.get("status")

        response = test_client.delete('/products/' + api_version)

        assert 200 == response.status_code
        json_data = response.json
        assert "success" == json_data.get("status")

        csv_file.seek(0, 0)
        response = test_client.put('/products/' + api_version, data=csv_file)

        assert 202 == response.status_code


@pytest.mark.parametrize("sku,input_params,expected_res",
                         [("help-return-art", {},
                           {"status": "success", "sku": "help-return-art", "code": 200}),

                          ("no-sku-here", {},
                           {"status": "failure", "errorCode": "NOT_FOUND", "code": 404}),

                          ("help-return-art", {"status": "active"},
                           {"status": "failure", "errorCode": "NOT_FOUND", "code": 404}),

                          (None, {"name": "lauren"},
                           {"status": "success", "sku": "grow-we-decide-job", "code": 200}),

                          (None, {"limit": 5, "page": 3, "status": "active"},
                           {"status": "failure", "errorCode": "NOT_FOUND", "code": 404}),
                          ])
def test_product_search(test_client, sku, input_params, expected_res):
    if sku is None:
        response = test_client.get('/products/' + api_version, query_string=input_params)
    else:
        response = test_client.get('/products/' + api_version + sku, query_string=input_params)

    assert expected_res.get("code") == response.status_code
    json_data = response.json
    assert expected_res.get("status") == json_data.get("status")
    if json_data.get("status") == "success":
        assert expected_res.get("sku") == json_data.get("data")[0].get("sku")
    else:
        assert expected_res.get("errorCode") == json_data.get("errorCode")


@pytest.mark.parametrize("sku,input_params,expected_res",
                         [
                             ("everyone-budget", {"status": "active"},
                              {"status": "success", "code": 200}),
                             ("un-known", {"status": "active"},
                              {"status": "failure", "errorCode": "NOT_FOUND", "code": 404})
                         ])
def test_product_mark(test_client, sku, input_params, expected_res):
    response = test_client.patch('/products/' + api_version + sku, query_string=input_params)

    assert expected_res.get("code") == response.status_code
    json_data = response.json
    assert expected_res.get("status") == json_data.get("status")
    if json_data.get("status") != "success":
        assert expected_res.get("errorCode") == json_data.get("errorCode")
