def test_s3_client_list_buckets(TestClient):
    res = TestClient.post('/client/s3/list_buckets')
    print(res)


def test_s3_client_list_objects_v2(TestClient):
    payload = dict(
        Bucket='',
    )
    res = TestClient.post('/client/s3/list_objects_v2', json=payload)
    print(res)
