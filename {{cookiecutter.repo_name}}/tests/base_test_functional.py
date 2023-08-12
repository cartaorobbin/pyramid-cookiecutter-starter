def test_root(testapp):
    res = testapp.get('/', status=200)
    assert b'Pyramid' in res.body

def test_notfound(testapp):
    res = testapp.get('/badurl', status=404)
    assert res.status_code == 404


def test_health(testapp):
    res = testapp.get('/health', status=200)
    assert res.json == {"status": "true"}
