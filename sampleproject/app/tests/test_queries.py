import pytest
from graphene.test import Client

from sampleproject.schema import schema
from .factories import UserFactory


@pytest.fixture()
def batch():
    UserFactory.create_batch(50)
    UserFactory.create(
        last_name='Wayne',
    )


@pytest.mark.django_db()
def test_DjangoListObjectField(batch):
    client = Client(schema)
    executed = client.execute("""{
      allUsers {
        results(limit:5, offset:5){
          id
          username
          firstName
          lastName
        }
        totalCount
      }
    }""")

    results = executed['data']['allUsers']['results']
    assert len(results) == 5


@pytest.mark.django_db()
@pytest.mark.parametrize('last_name,count', [
    ['Doe', 5],
    ['Wayne', 1],
])
def test_DjangoFilterPaginateListField(batch, last_name, count):
    client = Client(schema)
    executed = client.execute("""{
      allUsers1(lastName_Iexact:"%s", limit:5, offset:0){
        username
        id
      }
    }""" % last_name)

    results = executed['data']['allUsers1']
    assert len(results) == count
