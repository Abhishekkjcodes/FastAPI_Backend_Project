from app import schemas
import pytest
def test_get_all_posts(authorized_client,test_posts):
    res=authorized_client.get("/posts/")
    def validate(post):
        return schemas.PostStatsResponse(**post)
    posts_map=list(map(validate,res.json()))
    assert res.status_code==200
    assert len(res.json())==len(test_posts)
    for post in posts_map:
        assert post.likes==0
        assert post.dislikes==0

def test_unauth_get_all_posts(client):
    res=client.get("/posts/")
    assert res.status_code==401

def test_unauth_get_one_posts(client,test_posts):
    res=client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code==401

def test_get_one_post_not_exist(authorized_client):
    res=authorized_client.get("posts/4") #only 3 posts so no
    assert res.status_code==404

def test_get_one_post(authorized_client,test_posts):
    res=authorized_client.get(f"/posts/{test_posts[0].id}")
    post=schemas.PostStatsResponse(**res.json())
    assert post.Post.title==test_posts[0].title
    assert res.status_code==200

@pytest.mark.parametrize("title,content,published",[
    ("new post","new content",True),
    ("awesome new title","awesome new content",False),
    ("dunkins","its a donut place",True)])
def test_create_post(authorized_client,test_user,title,content,published):
    res=authorized_client.post("/posts/",json={"title":title,"content":content,"published":published})
    assert res.status_code==201
    post=schemas.PostResponse(**res.json())
    assert post.title==title
    assert post.content==content
    assert post.published==published
    assert post.user_id==test_user['id']

def test_create_post_published_default(authorized_client,test_user):
    res=authorized_client.post("/posts/",json={"title":"random titlle","content":"random content"})
    assert res.status_code==201
    post=schemas.PostResponse(**res.json())
    assert post.title=="random titlle"
    assert post.content=="random content"
    assert post.published==True
    assert post.user_id==test_user['id']

def test_unauth_create_post(client):
    res=client.post("/posts/",json={"title":"random titlle","content":"random content"})
    assert res.status_code==401

def test_unauth_delete_post(client,test_posts,test_user):
    res=client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code==401

def test_delete_post(authorized_client,test_posts,test_user):
    res=authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code==204

def test_delete_post_not_exist(authorized_client,test_posts,test_user):
    res=authorized_client.delete("/posts/888")
    assert res.status_code==404

def test_delete_other_user_post(test_user,test_user2,test_posts,authorized_client):
    res=authorized_client.delete(f"/posts/{test_posts[3].id}")
    assert res.status_code==403


def test_update_post(authorized_client, test_user, test_posts):
    data = {
    "title": "updated title",
    "content": "updatd content",
    "id": test_posts[0].id
    }
    res=authorized_client.put(f"/posts/{test_posts[0].id}", json=data)
    updated_post=schemas.PostResponse(**res.json())
    assert res.status_code==200
    assert updated_post.title==test_posts[0].title
    assert updated_post.title==data["title"]

def test_update_other_user_post(authorized_client,test_user2, test_user, test_posts):
    data = {
    "title": "updated title",
    "content": "updatd content",
    "id": test_posts[3].id
    }
    res=authorized_client.put(f"/posts/{test_posts[3].id}", json=data)
    assert res.status_code==403

def test_unauth_update_post(client,test_posts,test_user):
    res=client.put(f"/posts/{test_posts[0].id}")
    assert res.status_code==401

def test_update_post_not_exist(authorized_client,test_posts,test_user):
    data = {
    "title": "updated title",
    "content": "updatd content",
    "id": test_posts[0].id
    }
    res=authorized_client.put("/posts/888", json=data)
    assert res.status_code==404
