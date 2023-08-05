<div align="center">
    <h1>Python Serverside</h1>
</div>

# About

A Python serverside toolkit for fast and secure server-side programming with python.

## Installation

```bash
pip3 install serverside
```

## Usage

The following outlines the current features of this toolkit. This toolkit was developed
with one thing in mind:

 > To keep everything flexible so you can     inject your own logic where nescessary, and to use other popular packages so there isn't another library you have to get familiar with.

That means that this toolkit makes extensive use of these packages: _Django, aiohttp, Ariadne, djangorestframework_.

### GraphQL

GraphQL is a fantastic way to build API's that consume less of the backend
developers time. We are a fan of [Ariadne GraphQL](https://ariadnegraphql.org). Schema first development is our
favourite way of developing graphql applications, and allow for alot more flexibility compared to libraries such as _graphene_.

We wanted the ability to almost directly generate the logic for CRUD operations from defined Django models, but still keep it flexible for additional logic.

_NOTE: Our automatic resolvers use Relay, as in practice it has superior pagination
abilities. You can find more information [here](https://facebook.github.io/relay/graphql/connections.htm)_.

So let's say we have a (very simple) Django user model in `models.py`:

```python
from django.db import models

class User(models.Model):
    class Meta:
        ordering = ("-updated",)
        db_table = "users__users"

    id = models.CharField(primary_key=True, max_length=64)
    username = models.CharField(max_length=32, unique=True, null=False, blank=False)
    password = models.CharField(max_length=255, null=False, blank=False)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
```

We can now define a new file along side `models.py` called `resolvers.py`. Which looks like this:

```python
import typing as ty
import uuid
from ariadne import ObjectType
from serverside.graphql.ariadne_helpers import (
    BaseResolver, django_get_one, django_get_many,
    django_create, django_update, django_delete
)
from apps.users.models import User
from django.conf import settings

class UserResolvers(BaseResolver):

    user = ObjectType("User")

    @staticmethod
    @user.field("usernameModified")  # A custom attribute not defined on the Model
    async def get_modified_username(obj, *args, **kwargs):
        return obj.username + "_modified"

    @staticmethod
    @settings.QUERY.field("login")
    async def resolve_login(_, info, username: str, password: str):
        # Here would be your custom login logic
        return {"error": False, "message": "Successfull Login.", "token": "123"}

    @staticmethod
    @settings.QUERY.field("user")
    async def resolve_get(_, info, id: str):
        return await django_get_one(info, User, id)

    @staticmethod
    @settings.QUERY.field("users")
    async def resolve_list(_, info, *args, **kwargs):
        return await django_get_many(info, User, "users", kwargs)

    @staticmethod
    @settings.QUERY.field("createUser")
    async def resolve_create(_, info, id: str):
        return await django_create(info, User, id, lambda: str(uuid.uuid4()))  # Custom pk generator

    @staticmethod
    @settings.QUERY.field("updateUsers")
    async def resolve_update(_, info, *args, **kwargs):
        return await django_update(info, User, "users", kwargs)

    @staticmethod
    @settings.QUERY.field("deleteUser")
    async def resolve_delete(_, info, id: str):
        return await django_delete(info, User, id)


def export_resolvers() -> ty.List:
    return [
        UserResolvers
    ]
```

Now, to use this, in your Django settings file, you just need to add two lines:

```python
from ariadne import QueryType, MutationType

QUERY = QueryType()
MUTATION = MutationType()
```

And where you normally define your Ariadne schema, you can add the following:

```python
import ariadne
from apps.users.resolvers import export_resolvers as export_user_resolvers

resolvers = []
resolvers.extend(export_user_resolvers().export_resolvers())

schema = open("/path/to/schema.graphql", "r").read()
schema = ariadne.make_executable_schema(
    schema,
    [
        settings.QUERY,
        settings.MUTATION,
        *resolvers
    ]
```

And that's it. Assuming your `schema.graphql` has been updated, for the example above we may see:

```graphql
type User extends Node {
    id: ID
    username: String
    usernameModified: String
    password: String
    updated: Datetime
    created: Datetime
}

type Query {
    login(username: String!, password: String!): LoginResponse!
    user(id: String): User!
    users(
        first: Int, after: Int, before: Int, sortBy: String, sortDirection: String,
        username: String, username__startswith: String, username__istartswith: String,
        username__endswith: String, username__iendswith: String, username__contains: String, username__icontains: String,
    ): UserConnection!
}

type Mutation {
    createUser(input: UserInput!): UserPayload
    updateUser(id: ID!, prevUpdated: Float!, input: UserInput!): UserPayload
    deleteUser(id: ID!): BasicPayload
}
```

With that little amount of code, we now have a lot of standard logic already implemented.

### GraphQL: Technical Details

For the technical people out there, for `django_get_many`, the graphql syntax of the arguments directly relates to how Django filters.

We have also made the SQL queries only fetch data that is needed. Typically many
graphql libraries fetch all columns from the database, and then filter out what is
needed before passing back to the client. `django_get_one` and `django_get_many`, know what is being queried from the request, and specifically only fetch those columns from the database

For `ForeignKey` and `ManyToMany` relationships, we make extensive use of Django prefetching capabilities, so that the SQL queries are at the absolute minimum.

Because python is snake case, but graphql is camelcase, we have already taken care of automatically converting between the two.
