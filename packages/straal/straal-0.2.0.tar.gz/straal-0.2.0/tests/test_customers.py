import datetime
import json

import pytest
import responses

import straal
from straal import exceptions


@responses.activate
def test_customer_create_missing_email_fail(straal_base_url):
    url = fr"{straal_base_url}v1/customers"
    err_json = {"errors": [{"code": 12001, "message": "Missing customer email"}]}
    responses.add(responses.POST, url, json=err_json, status=400)

    with pytest.raises(exceptions.customer.MissingCustomerEmail):
        straal.Customer.create(email=None)

    assert len(responses.calls) == 1
    straal_request = json.loads(responses.calls[0].request.body)
    assert straal_request == {"email": None}


@responses.activate
def test_customer_create_invalid_email_fail(straal_base_url):
    url = fr"{straal_base_url}v1/customers"
    err_json = {"errors": [{"code": 12002, "message": "Invalid email"}]}
    responses.add(responses.POST, url, json=err_json, status=400)

    invalid_email = "customer@invalid"
    with pytest.raises(exceptions.customer.InvalidEmail):
        straal.Customer.create(email=invalid_email)

    assert len(responses.calls) == 1
    straal_request = json.loads(responses.calls[0].request.body)
    assert straal_request == {"email": invalid_email}


@responses.activate
def test_customer_create_email_too_long_fail(straal_base_url):
    url = fr"{straal_base_url}v1/customers"
    err_json = {
        "errors": [{"code": 12003, "message": "Customer email too long (maxlen: 150)"}]
    }

    responses.add(responses.POST, url, json=err_json, status=400)

    incredibly_long_email = f"{'a' * 150}@example.net"
    with pytest.raises(exceptions.customer.EmailTooLong):
        straal.Customer.create(email=incredibly_long_email)

    assert len(responses.calls) == 1
    straal_request = json.loads(responses.calls[0].request.body)
    assert straal_request == {"email": incredibly_long_email}


@responses.activate
def test_customer_create_email_too_short_fail(straal_base_url):
    url = fr"{straal_base_url}v1/customers"
    err_json = {
        "errors": [
            {"code": 12004, "message": "Customer email too short (minlen: 5)"},
            {"code": 12002, "message": "Invalid email"},
        ]
    }

    responses.add(responses.POST, url, json=err_json, status=400)

    with pytest.raises(exceptions.customer.EmailTooShort):
        straal.Customer.create(email="a@b")

    assert len(responses.calls) == 1
    straal_request = json.loads(responses.calls[0].request.body)
    assert straal_request == {"email": "a@b"}


@responses.activate
def test_customer_create_reference_exists_fail(straal_base_url, customer_json):
    url = fr"{straal_base_url}v1/customers"
    err_json = {
        "errors": [
            {"code": 12005, "message": "Customer with this reference already exists"}
        ]
    }
    responses.add(responses.POST, url, json=err_json, status=400)

    reference = "existing-reference"
    with pytest.raises(exceptions.customer.ReferenceAlreadyExists):
        straal.Customer.create(email=customer_json["email"], reference=reference)

    assert len(responses.calls) == 1
    straal_request = json.loads(responses.calls[0].request.body)
    assert straal_request == {"email": customer_json["email"], "reference": reference}


@responses.activate
def test_customer_create_reference_too_long_fail(straal_base_url, customer_json):
    url = fr"{straal_base_url}v1/customers"
    err_json = {
        "errors": [
            {"code": 12006, "message": "Customer reference too long (maxlen: 32)"}
        ]
    }
    responses.add(responses.POST, url, json=err_json, status=400)

    reference = "A" * 33
    with pytest.raises(exceptions.customer.ReferenceTooLong):
        straal.Customer.create(email=customer_json["email"], reference=reference)

    assert len(responses.calls) == 1
    straal_request = json.loads(responses.calls[0].request.body)
    assert straal_request == {"email": customer_json["email"], "reference": reference}


@responses.activate
def test_customer_create_success(straal_base_url, customer_json):
    url = fr"{straal_base_url}v1/customers"
    responses.add(responses.POST, url, json=customer_json)

    customer = straal.Customer.create(
        email=customer_json["email"], reference=customer_json["reference"]
    )

    assert len(responses.calls) == 1
    straal_request = json.loads(responses.calls[0].request.body)
    assert straal_request == {
        "email": customer_json["email"],
        "reference": customer_json["reference"],
    }

    assert customer.id == customer_json["id"]
    assert customer.email == customer_json["email"]
    assert customer.reference == customer_json["reference"]
    created_at = datetime.datetime.utcfromtimestamp(customer_json["created_at"])
    assert customer.created_at == created_at
    assert customer.last_transaction is None


@responses.activate
def test_customer_create_without_reference_success(straal_base_url, customer_json):
    customer_json["reference"] = None
    url = fr"{straal_base_url}v1/customers"
    responses.add(responses.POST, url, json=customer_json)

    customer = straal.Customer.create(email=customer_json["email"])

    assert len(responses.calls) == 1
    straal_request = json.loads(responses.calls[0].request.body)
    assert straal_request == {"email": customer_json["email"]}

    assert customer.id == customer_json["id"]
    assert customer.email == customer_json["email"]
    assert customer.reference is None
    created_at = datetime.datetime.utcfromtimestamp(customer_json["created_at"])
    assert customer.created_at == created_at
    assert customer.last_transaction is None


@responses.activate
def test_existing_customer_get_success(straal_base_url, customer_json):
    url = fr"{straal_base_url}v1/customers/{customer_json['id']}"
    responses.add(responses.GET, url, json=customer_json)

    customer = straal.Customer.get(customer_json["id"])

    assert len(responses.calls) == 1
    straal_request = responses.calls[0].request
    assert straal_request.body is None

    assert customer.id == customer_json["id"]
    assert customer.email == customer_json["email"]
    assert customer.reference == customer_json["reference"]
    created_at = datetime.datetime.utcfromtimestamp(customer_json["created_at"])
    assert customer.created_at == created_at
    assert customer.last_transaction is None


@responses.activate
def test_list_customers_success(straal_base_url, customer_list_json):
    url = fr"{straal_base_url}v1/customers"
    responses.add(responses.GET, url, json=customer_list_json)

    customer_list = straal.Customer.list()

    assert len(responses.calls) == 1
    straal_request = responses.calls[0].request
    assert straal_request.body is None

    assert isinstance(customer_list, list)
    assert len(customer_list) == 2

    assert customer_list[0].id == customer_list_json["data"][0]["id"]
    assert customer_list[0].email == customer_list_json["data"][0]["email"]
    assert customer_list[0].reference == customer_list_json["data"][0]["reference"]
    created_at_ts = customer_list_json["data"][0]["created_at"]
    created_at = datetime.datetime.utcfromtimestamp(created_at_ts)
    assert customer_list[0].created_at == created_at
    assert customer_list[0].last_transaction is None

    assert customer_list[1].id == customer_list_json["data"][1]["id"]
    assert customer_list[1].email == customer_list_json["data"][1]["email"]
    assert customer_list[1].reference == customer_list_json["data"][1]["reference"]
    created_at_ts = customer_list_json["data"][1]["created_at"]
    created_at = datetime.datetime.utcfromtimestamp(created_at_ts)
    assert customer_list[1].created_at == created_at
    assert customer_list[1].last_transaction is None


@responses.activate
def test_list_customers_empty_success(straal_base_url):
    url = fr"{straal_base_url}v1/customers"
    empty_list_json = {"page": 1, "per_page": 30, "total_count": 0, "data": []}
    responses.add(responses.GET, url, json=empty_list_json)

    customer_list = straal.Customer.list()

    assert len(responses.calls) == 1
    straal_request = responses.calls[0].request
    assert straal_request.body is None

    assert customer_list == []


@responses.activate
def test_list_customers_invalid_filter_fail(straal_base_url, customer_list_json):
    url = fr"{straal_base_url}v1/customers"
    responses.add(responses.GET, url, json=customer_list_json)

    with pytest.raises(RuntimeError):
        straal.Customer.list("id==100")

    assert len(responses.calls) == 0


@responses.activate
def test_list_customers_filter_kwarg_fail(straal_base_url, customer_list_json):
    url = fr"{straal_base_url}v1/customers"
    responses.add(responses.GET, url, json=customer_list_json)

    with pytest.raises(TypeError):
        straal.Customer.list(filters=["id==100"])

    assert len(responses.calls) == 0


@responses.activate
def test_list_customers_eq_filter_id_success(straal_base_url, customer_list_json):
    customer_list_json["data"].pop(1)
    customer_dict = customer_list_json["data"][0]
    url = fr"{straal_base_url}v1/customers"
    responses.add(responses.GET, url, json=customer_list_json)

    customer_list = straal.Customer.list(straal.filters.ID == customer_dict["id"])

    assert len(responses.calls) == 1
    straal_request = responses.calls[0].request
    assert straal_request.url == f"{url}?id__eq={customer_dict['id']}"
    assert straal_request.body is None

    assert isinstance(customer_list, list)
    assert len(customer_list) == 1

    assert customer_list[0].id == customer_dict["id"]
    assert customer_list[0].email == customer_dict["email"]
    assert customer_list[0].reference == customer_dict["reference"]
    created_at = datetime.datetime.utcfromtimestamp(customer_dict["created_at"])
    assert customer_list[0].created_at == created_at
    assert customer_list[0].last_transaction is None


@responses.activate
def test_list_customers_ne_filter_id_success(straal_base_url, customer_list_json):
    customer_dict = customer_list_json["data"].pop(0)
    url = fr"{straal_base_url}v1/customers"
    responses.add(responses.GET, url, json=customer_list_json)

    customer_list = straal.Customer.list(straal.filters.ID != customer_dict["id"])

    assert len(responses.calls) == 1
    straal_request = responses.calls[0].request
    assert straal_request.url == f"{url}?id__ne={customer_dict['id']}"
    assert straal_request.body is None

    assert isinstance(customer_list, list)
    assert len(customer_list) == 1

    assert customer_list[0].id == customer_list_json["data"][0]["id"]
    assert customer_list[0].email == customer_list_json["data"][0]["email"]
    assert customer_list[0].reference == customer_list_json["data"][0]["reference"]
    created_at_ts = customer_list_json["data"][0]["created_at"]
    created_at = datetime.datetime.utcfromtimestamp(created_at_ts)
    assert customer_list[0].created_at == created_at
    assert customer_list[0].last_transaction is None
