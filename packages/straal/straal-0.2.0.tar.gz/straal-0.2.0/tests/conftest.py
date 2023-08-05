import pytest


@pytest.fixture(scope="session")
def straal_base_url():
    return "https://straal/"


@pytest.fixture(autouse=True, scope="function")
def env_test_setup(monkeypatch, straal_base_url):
    """
    Makes sure tests will never fire requests to actual server
    """
    import straal

    straal.init("DUMMY_TEST_API_KEY", straal_base_url)


@pytest.fixture(scope="function")
def customer_json():
    return {
        "id": "cus_123",
        "created_at": 1575376785,
        "email": "customer@example.net",
        "reference": "SOME_ID",
    }


@pytest.fixture(scope="function")
def customer_list_json():
    return {
        "page": 1,
        "per_page": 30,
        "total_count": 2,
        "data": [
            {
                "id": "cus_123",
                "created_at": 1575376785,
                "email": "customer@example.net",
                "reference": "SOME_ID",
            },
            {
                "id": "cus_987",
                "created_at": 1575377785,
                "email": "other_customer@example.net",
                "reference": "SOME_OTHER_ID",
            },
        ],
    }


@pytest.fixture(scope="function")
def visa_card_json():
    return {
        "id": "card_123",
        "customer": {"id": "cus_123"},
        "created_at": 1575377785,
        "brand": "visa",
        "name": "John Smith",
        "num_bin": "444444",
        "num_last_4": "4448",
        "expiry_month": 11,
        "expiry_year": 2020,
        "origin_ipaddr": "192.0.2.1",
        "extra_data": {},
        "straal_custom_data": {},
        "state": "active",
        "state_flags": [],
        "transactions": [],
    }
