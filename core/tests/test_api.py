

# def test_for_equality1():
#     assert 1 == 1

                                                         # برای اینکه کار کنه توی ترمینال بزن pytest test_api.py -v

# def test_for_equality2():
#     assert 2 == 2


 

# def test_read_main():
#     response = client.get("/")
#     assert response.status_code == 200
#     assert response.json() == {"Message" : "Hello World"}
 


def test_login_response_401(anon_client):
    payload = {
        "username":"mahdi",
        "password":"12341234"
    }

    response = anon_client.post("/users/login", json=payload)
    assert response.status_code == 401



def test_login_response_200(anon_client):
    payload = {
        "username":"mahdi",
        "password":"12341234"
    }

    response = anon_client.post("/users/login", json=payload)
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()




def test_register_response_201(anon_client):
    payload = {
        "username":"alibigdeli",
        "password":"12341234",
        "confirm_password":"12341234"
    }

    response = anon_client.post("/users/register", json=payload)
    assert response.status_code == 201