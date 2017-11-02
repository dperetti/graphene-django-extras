import graphene
from django.contrib.auth.models import User
from graphene_django import DjangoObjectType
from graphene_django_extras import DjangoListObjectType, \
    DjangoInputObjectType, \
    LimitOffsetGraphqlPagination, \
    DjangoFilterPaginateListField


class UserType(DjangoObjectType):
    class Meta:
        model = User
        description = " Type definition for a single user "
        filter_fields = {
            'id': ['exact', ],
            'first_name': ['icontains', 'iexact'],
            'last_name': ['icontains', 'iexact'],
            'username': ['icontains', 'iexact'],
            'email': ['icontains', 'iexact']
        }


class UserListType(DjangoListObjectType):
    class Meta:
        description = " Type definition for user list "
        model = User
        pagination = LimitOffsetGraphqlPagination(max_limit=20)


class UserInput(DjangoInputObjectType):
    class Meta:
        description = ("User InputType definition to use as input on an "
                       "Arguments class on traditional Mutations ")
        model = User


class UserMutation(graphene.Mutation):
    """
    On traditional mutations, classes definition you must implement
    the mutate function
    mutation myMutation {
        traditionalUserMutation(newUser: {
          username: "dodo", password: "passpasspass", email: "dom@dom.com"}) {
            user {
            id
          }
        }
    }
    """
    user = graphene.Field(UserType, required=False)

    class Arguments:
        new_user = graphene.Argument(UserInput)

    class Meta:
        description = " Graphene traditional mutation for Users "

    @staticmethod
    def mutate(self, info, new_user):
        username = new_user['username']
        email = new_user['email']
        password = new_user['password']
        user = User.objects.create_user(username, email, password)
        return UserMutation(user=user)


class Query(graphene.ObjectType):
    # all_users = DjangoListObjectField(UserListType, description='All Users query')
    all_users1 = DjangoFilterPaginateListField(UserType, pagination=LimitOffsetGraphqlPagination())


class Mutations(graphene.ObjectType):
    traditional_user_mutation = UserMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutations)
