import pytest

@pytest.mark.parametrize("post_id,direction",[(1,1),(1,-1),(2,-1),(3,-1),(3,1)])
def test_vote_post(authorized_client,test_user,test_posts,post_id,direction):
    res=authorized_client.post("/likes/",json={"post_id":post_id,"direction":direction})
    assert res.status_code==200
    reaction = "liked" if direction == 1 else "disliked"
    assert res.json()=={"message": f"You {reaction} the post"}

@pytest.mark.parametrize("post_id,direction",[(1,1),(1,-1),(2,-1)])
def test_remove_like(authorized_client,test_user,test_posts,post_id,direction):
    res = authorized_client.post("/likes/",json={"post_id": post_id, "direction": direction})
    reaction = "liked" if direction == 1 else "disliked"
    assert res.json()=={"message": f"You {reaction} the post"}
    res = authorized_client.post("/likes/",json={"post_id": post_id, "direction": direction})
    assert res.json() == {"message": "Your reaction was removed from the post"}

def test_unauth_vote_post(client,test_user,test_posts,):
    res=client.post("/likes/",json={"post_id":test_posts[0].id,"direction":1})
    assert res.status_code==401

def test_vote_post_not_exist(authorized_client):
    res=authorized_client.post("/likes/",json={"post_id":8888888,"direction":1})
    assert res.status_code==404