from urllib.parse import quote

from src.app import activities


def test_get_activities(client):
    # Arrange
    expected_activity_names = set(activities.keys())

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    assert set(response.json().keys()) == expected_activity_names


def test_post_signup_success(client):
    # Arrange
    activity_name = "Swimming Club"
    new_email = "julia@mergington.edu"
    url = f"/activities/{quote(activity_name, safe='')}/signup"

    # Act
    response = client.post(url, params={"email": new_email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {new_email} for {activity_name}"}
    assert new_email in activities[activity_name]["participants"]


def test_post_signup_duplicate_rejected(client):
    # Arrange
    activity_name = "Chess Club"
    duplicate_email = "michael@mergington.edu"
    url = f"/activities/{quote(activity_name, safe='')}/signup"

    # Act
    response = client.post(url, params={"email": duplicate_email})

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_delete_unregister_success(client):
    # Arrange
    activity_name = "Chess Club"
    email_to_remove = "daniel@mergington.edu"
    url = f"/activities/{quote(activity_name, safe='')}/signup"
    assert email_to_remove in activities[activity_name]["participants"]

    # Act
    response = client.delete(url, params={"email": email_to_remove})

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Unregistered {email_to_remove} from {activity_name}"}
    assert email_to_remove not in activities[activity_name]["participants"]


def test_delete_unknown_participant_returns_404(client):
    # Arrange
    activity_name = "Chess Club"
    missing_email = "notthere@mergington.edu"
    url = f"/activities/{quote(activity_name, safe='')}/signup"

    # Act
    response = client.delete(url, params={"email": missing_email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found for this activity"
