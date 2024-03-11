def test_required_token_request_pass_by_header(client, api_key_header):
    response = client.get("/", headers=api_key_header)
    assert response.status_code == 200


def test_required_token_request_pass_by_url_param(client, api_key_header):
    response = client.get(f"/?api-key={api_key_header['x-api-key']}")
    assert response.status_code == 200


def test_missing_token_request(client):
    response = client.get("/")
    assert response.status_code == 401
