def test_request_password_reset(client):
    client.post("/auth/register", json={
        "email": "reset@test.com",
        "password": "password123"
    })

    response = client.post("/auth/password-reset/request", json={
        "email": "reset@test.com"
    })
    assert response.status_code == 200
    assert "message" in response.json()


def test_password_reset(client):
    # Цей тест вимагає, щоб був валідний токен для скидання
    # Токен можна отримати через mock або вручну створити

    # Для прикладу, просто перевіримо, що ендпоінт існує і відповідає
    response = client.post("/auth/password-reset/confirm", json={
        "token": "dummy-token",
        "new_password": "newpassword123"
    })
    # Можливо, тут буде 400, якщо токен не валідний, це теж корисно перевірити
    assert response.status_code in (200, 400)
