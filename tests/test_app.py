from fastapi import status


def test_root_redirects(client):
    response = client.get("/", follow_redirects=False)

    assert response.status_code == status.HTTP_307_TEMPORARY_REDIRECT
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_data(client):
    response = client.get("/activities")

    assert response.status_code == status.HTTP_200_OK
    assert "Chess Club" in response.json()
    assert response.json()["Chess Club"]["description"] == "Learn strategies and compete in chess tournaments"


def test_signup_adds_new_participant(client):
    response = client.post(
        "/activities/Chess%20Club/signup?email=newstudent@mergington.edu"
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["message"] == "Signed up newstudent@mergington.edu for Chess Club"

    activities_response = client.get("/activities")
    assert "newstudent@mergington.edu" in activities_response.json()["Chess Club"]["participants"]


def test_signup_duplicate_returns_error(client):
    response = client.post(
        "/activities/Chess%20Club/signup?email=michael@mergington.edu"
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_remove_participant(client):
    response = client.delete(
        "/activities/Chess%20Club/participants?email=michael@mergington.edu"
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["message"] == "Removed michael@mergington.edu from Chess Club"

    activities_response = client.get("/activities")
    assert "michael@mergington.edu" not in activities_response.json()["Chess Club"]["participants"]


def test_remove_missing_participant_returns_404(client):
    response = client.delete(
        "/activities/Chess%20Club/participants?email=doesnotexist@mergington.edu"
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Participant not found"
