import pytest
# from graphene.test import Client
# from sampleproject.app import schema


@pytest.mark.django_db
def test_mutation():
    # client = Client(schema)
    # executed = client.execute('''{ hey }''', context_value={'user': 'Peter'})

    assert True