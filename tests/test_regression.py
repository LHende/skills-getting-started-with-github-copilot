def test_signup_then_unregister_roundtrip(client):
    activity_name = "Science Club"
    email = "roundtrip@mergington.edu"

    signup_response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )
    assert signup_response.status_code == 200

    unregister_response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": email},
    )
    assert unregister_response.status_code == 200

    participants = client.get("/activities").json()[activity_name]["participants"]
    assert email not in participants
