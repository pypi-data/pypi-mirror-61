# FactoryMan

FactoryMan provides Django specific extensions for [Factory Boy](https://factoryboy.readthedocs.io/en/latest/introduction.html).

## Installation

`pip install factory-man`

## Usage

FactoryMan provides you with a factory function `create_populated_modelfactory`, which accepts the model class and automatically creates a factory class based on the model's fields. If you want to override some fields, you can pass them as keyword arguments to the `__init__` method.

```py
from factoryman import create_populated_modelfactory
from .models import Project

ProjectFactory = create_populated_modelfactory(Project)

ExpiredProjectFactory = create_populated_modelfactory(Project, deadline='1999-04-04')
```

To override the factory's `_create` method, use `create_override` keyword argument. This is useful to create many-to-many connections as described in the Factory Boy documentation.

Check out [this article](https://medium.com/insightfulsolutions/elegant-and-dry-test-data-creation-for-django-be68373c69d4?source=friends_link&sk=6d67a758e7d0b25c527df602b67aa051) for a more detailed user guide.

## Low-level Features

`ModelFieldSequence` extends `factory.Sequence` to provide a little more DRY syntax. It accepts a Django model class as parameter and uses the class name togeteher with the field name to which it is bound to for creating an unique value.

Alternatively, it can accept a `string` parameter, which will be used directly instead of a name derived from the class and field.

Example:

```py
from factory.django import DjangoModelFactory as ModelFactory
from factoryman import ModelFieldSequence


class CharityFactory(ModelFactory):
    class Meta:
        model = Charity

    name = ModelFieldSequence(Charity)  # Will be `Charity__name-n`, where n is the object count
    email = ModelFieldSequence(string='hello@charity.ee')  # Will be `hello@charity.ee-n`, where n is the object count
```
