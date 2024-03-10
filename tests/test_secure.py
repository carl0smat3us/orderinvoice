def test_required_token_request(client, api_key_header):
    response = client.get(f"/", headers=api_key_header)
    assert response.status_code == 200


def test_missing_token_request(client):
    response = client.get(f"/")
    assert response.status_code == 401
