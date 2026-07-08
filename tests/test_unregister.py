def test_unregister_removes_existing_participant(client):
    activity_name = "Tennis"
    email = "sarah@mergington.edu"

    before = client.get("/activities").json()[activity_name]["participants"]
    assert email in before

    response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": email},
    )

    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from {activity_name}"

    after = client.get("/activities").json()[activity_name]["participants"]
    assert len(after) == len(before) - 1
    assert email not in after


def test_unregister_rejects_unknown_activity(client):
    response = client.delete(
        "/activities/Unknown Activity/participants",
        params={"email": "student@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_rejects_not_signed_up_participant(client):
    response = client.delete(
        "/activities/Chess Club/participants",
        params={"email": "not.registered@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not signed up for this activity"
