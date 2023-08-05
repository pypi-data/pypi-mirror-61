import straal


def test_straal_config_is_mocked(straal_base_url):
    assert straal.get_api_key() == "DUMMY_TEST_API_KEY"
    assert straal.get_base_url() == straal_base_url
