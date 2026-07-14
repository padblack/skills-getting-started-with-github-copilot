import pytest


def test_get_activities_returns_all_activities(client):
    # Arrange
    expected_activity = "Chess Club"

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert expected_activity in data
    assert data[expected_activity]["description"] == "Learn strategies and compete in chess tournaments"


def test_signup_for_activity_adds_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "teststudent@mergington.edu"
    url = f"/activities/{activity_name}/signup?email={email}"

    # Act
    response = client.post(url)

    # Assert
    assert response.status_code == 200
    body = response.json()
    assert body["message"] == f"Signed up {email} for {activity_name}"

    response = client.get("/activities")
    activity = response.json()[activity_name]
    assert email in activity["participants"]


def test_signup_for_activity_returns_400_for_duplicate_signup(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    url = f"/activities/{activity_name}/signup?email={email}"

    # Act
    response = client.post(url)

    # Assert
    assert response.status_code == 400
    body = response.json()
    assert body["detail"] == "Student is already signed up for this activity"


def test_remove_participant_from_activity(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    url = f"/activities/{activity_name}/participants?email={email}"

    # Act
    response = client.delete(url)

    # Assert
    assert response.status_code == 200
    body = response.json()
    assert body["message"] == f"Removed {email} from {activity_name}"

    response = client.get("/activities")
    activity = response.json()[activity_name]
    assert email not in activity["participants"]


def test_remove_participant_returns_404_for_missing_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "nonexistent@mergington.edu"
    url = f"/activities/{activity_name}/participants?email={email}"

    # Act
    response = client.delete(url)

    # Assert
    assert response.status_code == 404
    body = response.json()
    assert body["detail"] == "Participant not found for this activity"
