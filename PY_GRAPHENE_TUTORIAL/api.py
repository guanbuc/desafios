# -*- encoding:utf-8 -*-


from flask_graphql import GraphQLView
from flask import Flask

from schema import schema


default_query = """
{
    allEmployees{
        edges{
            node{
            id
            name
            }
        }
    }
    allRoles{
        edges{
            node{
                roleId
                name
            }
        }
    }
    allDepartments{
        edges{
            node{
                id
                name
            }
        }
    }
}
"""


app = Flask(__name__)
app.debug = True


app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))


default_query = (default_query.replace(chr(10), ''))
#result = schema.execute(default_query)