def test_signup_adds_new_participant(client):
    activity_name = "Basketball"
    email = "new.student@mergington.edu"

    before = client.get("/activities").json()[activity_name]["participants"]
    assert email not in before

    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"

    after = client.get("/activities").json()[activity_name]["participants"]
    assert len(after) == len(before) + 1
    assert email in after


def test_signup_rejects_duplicate_participant(client):
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_rejects_unknown_activity(client):
    response = client.post(
        "/activities/Unknown Activity/signup",
        params={"email": "student@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_rejects_when_activity_is_full(client):
    activity_name = "Art Club"
    activities = client.get("/activities").json()

    # Fill the activity to capacity first.
    while len(activities[activity_name]["participants"]) < activities[activity_name]["max_participants"]:
        next_index = len(activities[activity_name]["participants"])
        client.post(
            f"/activities/{activity_name}/signup",
            params={"email": f"filler{next_index}@mergington.edu"},
        )
        activities = client.get("/activities").json()

    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": "late.student@mergington.edu"},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Activity is full"
