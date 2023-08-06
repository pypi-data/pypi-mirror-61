# ariadna #

A featureful map object that can take path-like keys to access nested keys or attributes.

## Examples ##

```python
from ariadna import Caja

configuration = Caja({
    'clients' : [
        {
            'name' : 'Joe',
            'lastname' : 'Doe',
            'addresses' : [
                {
                    'street' : '1st Mulholland Drive',
                    'city' : 'Redmond',
                    'state' : 'Washington',
                    'zip' : '12345'
                },
                {
                    'street' : '15101 Linea Drive',
                    'city' : 'Miami',
                    'state' : 'Florida',
                    'zip' : '67890'
                }
            ],
            'phone' : [
                '1-555-888-8888',
                '1-404-NOT-REAL'
            ],
            'age': '42'
        }
    ]
})

# now the values can be accessed using
print(configuration['clients.0.addresses.1.city']) # == Miami
print(configuration['clients/0/phone/1']) # == 1-404-NOT-REAL

```