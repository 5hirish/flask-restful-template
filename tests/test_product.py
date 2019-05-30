import pytest

# def test_product_import(test_client):
#
#
#     response = test_client.post('/')
#
#     json_data = response.json
#     assert response.status_code == 200
#     assert json_data.get("status") == "success"


@pytest.mark.parametrize("input_params,expected_res",
                         [({"sku": "help-return-art"},
                           {"status": "success", "sku": "help-return-art"}),

                          ({"sku": "no-sku-here"},
                           {"status": "failure", "errorCode": "NOT_FOUND"}),

                          ({"sku": "help-return-art", "status": "active"},
                           {"status": "failure", "errorCode": "NOT_FOUND"})
                          ])
def test_product_search(test_client, input_params, expected_res):

    response = test_client.get('/product/', query_string=input_params)
    json_data = response.json
    assert response.status_code == 200
    assert json_data.get("status") == expected_res.get("status")
    if json_data.get("status") == "success":
        assert json_data.get("data").get("sku") == expected_res.get("sku")
    else:
        assert json_data.get("errorCode") == expected_res.get("errorCode")


def test_product_fetch(test_client):

    response = test_client.get('/product/all')
    json_data = response.json
    assert response.status_code == 200
    assert json_data.get("totalProducts") == 19
    assert len(json_data.get("data")) == 5
    assert json_data.get("status") == "success"


# def test_product_delete(test_client):
#
#     response = test_client.delete('/product/')
#     json_data = response.json
#     assert response.status_code == 200
#     assert json_data.get("status") == "success"
