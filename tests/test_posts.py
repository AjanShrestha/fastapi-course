from app import schemas


def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")

    assert res.status_code == 200
    assert len(res.json()) == len(test_posts)

    def validate(post):
        return schemas.PostOut(**post)

    # asserting the correct response types
    posts_map = map(validate, res.json())
    posts_lists = list(posts_map)


def test_unauthorized_get_all_posts(client, test_posts):
    res = client.get("/posts/")

    assert res.status_code == 401
