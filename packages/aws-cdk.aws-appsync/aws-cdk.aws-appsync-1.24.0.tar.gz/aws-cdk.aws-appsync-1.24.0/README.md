## AWS AppSync Construct Library

<!--BEGIN STABILITY BANNER-->---


![Stability: Experimental](https://img.shields.io/badge/stability-Experimental-important.svg?style=for-the-badge)

> **This is a *developer preview* (public beta) module. Releases might lack important features and might have
> future breaking changes.**
>
> This API is still under active development and subject to non-backward
> compatible changes or removal in any future version. Use of the API is not recommended in production
> environments. Experimental APIs are not subject to the Semantic Versioning model.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

## Usage Example

Given the following GraphQL schema file `schema.graphql`:

```graphql
type Customer {
    id: String!
    name: String!
}

input SaveCustomerInput {
    name: String!
}

type Query {
    getCustomers: [Customer]
    getCustomer(id: String): Customer
}

type Mutation {
    addCustomer(customer: SaveCustomerInput!): Customer
    saveCustomer(id: String!, customer: SaveCustomerInput!): Customer
    removeCustomer(id: String!): Customer
}
```

the following CDK app snippet will create a complete CRUD AppSync API:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
class ApiStack(Stack):
    def __init__(self, scope, id):
        super().__init__(scope, id)

        user_pool = UserPool(self, "UserPool",
            sign_in_type=SignInType.USERNAME
        )

        api = GraphQLApi(self, "Api",
            name="demoapi",
            log_config={
                "field_log_level": FieldLogLevel.ALL
            },
            user_pool_config={
                "user_pool": user_pool,
                "default_action": UserPoolDefaultAction.ALLOW
            },
            schema_definition_file="./schema.graphql"
        )

        customer_table = Table(self, "CustomerTable",
            billing_mode=BillingMode.PAY_PER_REQUEST,
            partition_key={
                "name": "id",
                "type": AttributeType.STRING
            }
        )
        customer_dS = api.add_dynamo_db_data_source("Customer", "The customer data source", customer_table)
        customer_dS.create_resolver(
            type_name="Query",
            field_name="getCustomers",
            request_mapping_template=MappingTemplate.dynamo_db_scan_table(),
            response_mapping_template=MappingTemplate.dynamo_db_result_list()
        )
        customer_dS.create_resolver(
            type_name="Query",
            field_name="getCustomer",
            request_mapping_template=MappingTemplate.dynamo_db_get_item("id", "id"),
            response_mapping_template=MappingTemplate.dynamo_db_result_item()
        )
        customer_dS.create_resolver(
            type_name="Mutation",
            field_name="addCustomer",
            request_mapping_template=MappingTemplate.dynamo_db_put_item("id", "customer"),
            response_mapping_template=MappingTemplate.dynamo_db_result_item()
        )
        customer_dS.create_resolver(
            type_name="Mutation",
            field_name="saveCustomer",
            request_mapping_template=MappingTemplate.dynamo_db_put_item("id", "customer", "id"),
            response_mapping_template=MappingTemplate.dynamo_db_result_item()
        )
        customer_dS.create_resolver(
            type_name="Mutation",
            field_name="removeCustomer",
            request_mapping_template=MappingTemplate.dynamo_db_delete_item("id", "id"),
            response_mapping_template=MappingTemplate.dynamo_db_result_item()
        )
```
