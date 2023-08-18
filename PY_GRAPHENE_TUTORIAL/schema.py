# -*- encoding:utf-8 -*-


import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType

from models import Department as DepartmentModel, Employee as EmployeeModel, Role as RoleModel


class Department(SQLAlchemyObjectType):
    class Meta:
        model = DepartmentModel
        interfaces = (relay.Node,)

class Employee(SQLAlchemyObjectType):
    class Meta:
        model = EmployeeModel
        interfaces = (relay.Node,)

class Role(SQLAlchemyObjectType):
    class Meta:
        model = RoleModel
        interfaces = (relay.Node,)


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    all_departments = SQLAlchemyConnectionField(Department.connection)
    all_employees = SQLAlchemyConnectionField(Employee.connection)
    all_roles = SQLAlchemyConnectionField(Role.connection)


schema = graphene.Schema(query=Query)