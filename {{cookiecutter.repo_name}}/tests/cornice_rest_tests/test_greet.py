



def test_greet(testapp):

    resp = testapp.get('/api/v1/greet', status=200)

    assert resp.json == {'hello': 'world'}


