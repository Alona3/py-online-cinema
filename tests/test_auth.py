def test_register_user(client):
    response = client.post("/auth/register", json={
        "email": "test@example.com",
        "password": "strongpassword123"
    })
    assert response.status_code == 201
    data = response.json()
    assert "email" in data
    assert data["email"] == "test@example.com"


def test_login_user(client):
    # спочатку зареєструємо користувача
    client.post("/auth/register", json={
        "email": "login@test.com",
        "password": "mypassword123"
    })

    response = client.post("/auth/login", data={
        "username": "login@test.com",
        "password": "mypassword123"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
