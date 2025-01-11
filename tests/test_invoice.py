from random import randint


def test_get_invoice_sucess(client, api_key_header):
    response = client.get("/invoice/1", headers=api_key_header)
    assert response.status_code == 200


def test_get_invoice_error_404(client, api_key_header):
    response = client.get(
        f"/invoice/{randint(1000, 10000)}", headers=api_key_header)
    assert response.status_code == 404
