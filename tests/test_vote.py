
def test_vote_post_once(create_posts, authorized_client, create_vote):
    post_id = create_posts[1].id
    res = authorized_client.post("/vote/", json={
        "post_id": post_id,
        "dir": 1
    })
    assert res.status_code == 201


def test_vote_post_twice(create_posts, authorized_client, create_vote):
    post_id = create_posts[0].id
    res = authorized_client.post("/vote/", json={
        "post_id": post_id,
        "dir": 1
    })
    assert res.status_code == 409


def test_delete_post(create_posts, authorized_client, create_vote):
    post_id = create_posts[0].id
    res = authorized_client.post("/vote/", json={
        "post_id": post_id,
        "dir": 0
    })
    assert res.status_code == 201


def test_vote_post_non_exist(authorized_client):
    res = authorized_client.post(
        "/vote/", json={"post_id": 80000, "dir": 1})
    assert res.status_code == 404


def test_vote_unauthorized_user(client, create_posts):
    res = client.post(
        "/vote/", json={"post_id": create_posts[3].id, "dir": 1})
    assert res.status_code == 401

