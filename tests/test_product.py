import pytest


def test_product_import(test_client):

    test_csv_file = 'test_products.csv'

    with open(test_csv_file, 'r') as csv_file:

        response = test_client.post('/product/csv/import', data=csv_file)

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
                           {"status": "success", "sku": "grow-we-decide-job"})
                          ])
def test_product_search(test_client, input_params, expected_res):
    response = test_client.get('/product/', query_string=input_params)
    json_data = response.json
    assert response.status_code == 200
    assert json_data.get("status") == expected_res.get("status")
    if json_data.get("status") == "success":
        assert json_data.get("data")[0].get("sku") == expected_res.get("sku")
    else:
        assert json_data.get("errorCode") == expected_res.get("errorCode")


@pytest.mark.parametrize("input_params,expected_res",
                         [({"limit": 10, "page": 1},
                           {"status": "success", "len": 10}),

                          ({"limit": 5, "page": 3},
                           {"status": "success", "len": 5}),

                          ({"limit": 5, "page": 3, "status": "active"},
                           {"status": "failure", "errorCode": "NOT_FOUND"}),
                          ])
def test_product_fetch(test_client, input_params, expected_res):
    response = test_client.get('/product/all', query_string=input_params)
    json_data = response.json
    assert response.status_code == 200
    assert json_data.get("status") == expected_res.get("status")
    if json_data.get("status") == "success":
        assert json_data.get("totalProducts") == 19
        assert len(json_data.get("data")) == expected_res.get("len")
    else:
        assert json_data.get("errorCode") == expected_res.get("errorCode")


