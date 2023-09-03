def test_open_api(testapp):
    """
    Just assert that swagger openapi is up
    """

    resp = testapp.get('/api/v1/openapi.json', status=200)