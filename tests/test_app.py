from src.app import activities


# ---------------------------------------------------------------------------
# GET /activities
# ---------------------------------------------------------------------------

def test_get_activities_returns_all(client):
    # Arrange
    expected_activities = list(activities.keys())

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    for activity in expected_activities:
        assert activity in data


# ---------------------------------------------------------------------------
# POST /activities/{activity_name}/signup
# ---------------------------------------------------------------------------

def test_signup_success(client):
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Successfully signed up for {activity_name}"}
    assert email in activities[activity_name]["participants"]


def test_signup_duplicate_email(client):
    # Arrange
    activity_name = "Chess Club"
    email = "duplicate@mergington.edu"
    activities[activity_name]["participants"].append(email)

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_signup_activity_not_found(client):
    # Arrange
    activity_name = "Nonexistent Club"
    email = "student@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_invalid_email_returns_validation_error(client):
    # Arrange
    activity_name = "Chess Club"
    invalid_email = "not-an-email"

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={invalid_email}")

    # Assert
    assert response.status_code == 422


def test_signup_max_participants_exceeded(client):
    # Arrange
    activity_name = "Chess Club"
    max_p = activities[activity_name]["max_participants"]
    # Fill remaining spots
    existing = len(activities[activity_name]["participants"])
    for i in range(max_p - existing):
        activities[activity_name]["participants"].append(f"filler{i}@mergington.edu")

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email=overflow@mergington.edu")

    # Assert
    assert response.status_code == 400
    assert "full" in response.json()["detail"].lower() or "max" in response.json()["detail"].lower()


# ---------------------------------------------------------------------------
# DELETE /activities/{activity_name}/unregister
# ---------------------------------------------------------------------------

def test_unregister_success(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    assert email in activities[activity_name]["participants"]

    # Act
    response = client.delete(f"/activities/{activity_name}/unregister?email={email}")

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Successfully unregistered from {activity_name}"}
    assert email not in activities[activity_name]["participants"]


def test_unregister_not_registered(client):
    # Arrange
    activity_name = "Chess Club"
    email = "notregistered@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/unregister?email={email}")

    # Assert
    assert response.status_code == 400
    assert "not signed up" in response.json()["detail"]


def test_unregister_activity_not_found(client):
    # Arrange
    activity_name = "Nonexistent Club"
    email = "student@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/unregister?email={email}")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_invalid_email_returns_validation_error(client):
    # Arrange
    activity_name = "Chess Club"
    invalid_email = "not-an-email"

    # Act
    response = client.delete(f"/activities/{activity_name}/unregister?email={invalid_email}")

    # Assert
    assert response.status_code == 422
