import pytest
from django.urls import reverse
from django.contrib.auth.models import User

@pytest.mark.django_db
def test_login_view_success(client):
    # Creamos usuario en BD
    user = User.objects.create_user(username="testuser", password="12345")
    print("creado")

    url = reverse("login") 
    data = {
        "username": "testuser",
        "password": "12345",
    }
    

    response = client.post(url, data)

    assert response.status_code == 302  

    assert "_auth_user_id" in client.session


@pytest.mark.django_db
def test_login_view_fail_wrong_password(client):
    User.objects.create_user(username="testuser", password="12345")

    url = reverse("login")
    data = {
        "username": "testuser",
        "password": "wrongpass",
    }

    response = client.post(url, data)

    assert response.status_code == 200  
    assert "_auth_user_id" not in client.session