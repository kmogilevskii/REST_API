from app.schemas import PostOut


def test_all_posts(authorized_client, create_posts):
    res = authorized_client.get("/posts/")
    def validate(post):
        return PostOut(**post)
    posts_map = map(validate, res.json())
    posts_lst = list(posts_map)

    assert isinstance(res.json(), list)
    assert len(res.json()) == len(create_posts)
    assert posts_lst[0].Post.id == create_posts[0].id
    assert posts_lst[0].Post.owner_id == create_posts[0].owner_id
    assert posts_lst[0].Post.created_at == create_posts[0].created_at


def test_unauthorized_get_all_posts(client):
    res = client.get("/posts/")
    assert res.status_code == 401

def test_unauthorized_get_single_post(client, create_posts):
    res = client.get(f"/posts/{create_posts[0].id}")
    assert res.status_code == 401

def test_get_nonexist_post(authorized_client):
    res = authorized_client.get("/posts/9999")
    assert res.status_code == 404