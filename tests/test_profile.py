def test_get_profile(client):
    # спочатку реєструємо користувача
    client.post("/auth/register", json={
        "email": "profile@test.com",
        "password": "password123"
    })

    # логінимося
    login_resp = client.post("/auth/login", data={
        "username": "profile@test.com",
        "password": "password123"
    })
    token = login_resp.json()["access_token"]

    # отримуємо профіль
    response = client.get("/profile/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert "email" in data
    assert data["email"] == "profile@test.com"


def test_update_profile(client):
    client.post("/auth/register", json={
        "email": "update@test.com",
        "password": "password123"
    })

    login_resp = client.post("/auth/login", data={
        "username": "update@test.com",
        "password": "password123"
    })
    token = login_resp.json()["access_token"]

    response = client.put("/profile/me", headers={"Authorization": f"Bearer {token}"}, json={
        "full_name": "New Name",
        "bio": "Test bio",
        "birth_date": "1990-01-01"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["full_name"] == "New Name"
    assert data["bio"] == "Test bio"
