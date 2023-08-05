# straal-python

# Installation

```console
$ pip install -U straal
```

# Example

```pycon
>>> import straal
>>> straal.init("your_api_key")
>>> customer = straal.Customer.create(email="customer@example.net")
>>> customer.email == "customer@example.net"
True
>>> customer.id is not None
True
```
