def test_refresh_token(client):
    client.post("/auth/register", json={
        "email": "token@test.com",
        "password": "password123"
    })

    login_resp = client.post("/auth/login", data={
        "username": "token@test.com",
        "password": "password123"
    })
    refresh_token = login_resp.json().get("refresh_token")

    response = client.post("/auth/token/refresh", json={
        "refresh_token": refresh_token
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
