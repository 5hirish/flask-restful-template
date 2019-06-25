import pytest


def test_product_import(test_client):

    test_csv_file = 'tests/test_products.csv'

    with open(test_csv_file, 'r') as csv_file:

        response = test_client.put('/products/', data=csv_file)

        json_data = response.json
        assert response.status_code == 200
        assert json_data.get("status") == "success"


@pytest.mark.parametrize("input_params,expected_res",
                         [({"sku": "help-return-art"},
                           {"status": "success", "sku": "help-return-art"}),

                          ({"sku": "no-sku-here"},
                           {"status": "failure", "errorCode": "NOT_FOUND"}),

                          ({"sku": "help-return-art", "status": "active"},
                           {"status": "failure", "errorCode": "NOT_FOUND"}),

                          ({"name": "lauren"},
                           {"status": "success", "sku": "grow-we-decide-job"}),

                          ({"limit": 5, "page": 3, "status": "active"},
                           {"status": "failure", "errorCode": "NOT_FOUND"}),
                          ])
def test_product_search(test_client, input_params, expected_res):
    response = test_client.get('/products/', query_string=input_params)
    json_data = response.json
    assert response.status_code == 200
    assert json_data.get("status") == expected_res.get("status")
    if json_data.get("status") == "success":
        assert json_data.get("data")[0].get("sku") == expected_res.get("sku")
    else:
        assert json_data.get("errorCode") == expected_res.get("errorCode")

