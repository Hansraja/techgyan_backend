from typing import Any, Dict
from graphene_django.constants import MUTATION_ERRORS_FLAG
from graphene_django.utils.utils import set_rollback
from graphene_django.views import GraphQLView, HttpError
from graphql import GraphQLError, GraphQLFormattedError

from django.db import connection, transaction
from django.http import HttpResponseNotAllowed
from django.http.response import HttpResponseBadRequest
from graphql import (
    ExecutionResult,
    OperationType,
    execute,
    get_operation_ast,
    parse,
    validate_schema,
)
from graphql.error import GraphQLError
from graphql.validation import validate
from graphene_django.constants import MUTATION_ERRORS_FLAG
from graphene_django.utils.utils import set_rollback
from graphene_django.settings import graphene_settings

class RkFormattedError(GraphQLFormattedError):
    stack: Dict[str, Any]

class GraphQl(GraphQLView):
    graphiql_template = 'graphql/view.html'

    def get_response(self, request, data, show_graphiql=False):
        query, variables, operation_name, id = self.get_graphql_params(request, data)

        execution_result = self.execute_graphql_request(
            request, data, query, variables, operation_name, show_graphiql
        )

        if getattr(request, MUTATION_ERRORS_FLAG, False) is True:
            set_rollback()

        status_code = 200
        if execution_result:
            response = {}
            if execution_result.errors:
                set_rollback()
                response["errors"] = [
                    self.format_error(e) for e in execution_result.errors
                ]

            if execution_result.errors and any(
                not getattr(e, "path", None) for e in execution_result.errors
            ):
                status_code = 400
            else:
                response["data"] = execution_result.data

            if self.batch:
                response["id"] = id
                response["status"] = status_code

            result = self.json_encode(request, response, pretty=show_graphiql)
        else:
            result = None
        return result, status_code

    def execute_graphql_request(
        self, request, data, query, variables, operation_name, show_graphiql=False
    ):
        if not query:
            if show_graphiql:
                return None
            raise HttpError(HttpResponseBadRequest("Must provide query string."))

        schema = self.schema.graphql_schema # type: ignore

        schema_validation_errors = validate_schema(schema)
        if schema_validation_errors:
            return ExecutionResult(data=None, errors=schema_validation_errors)

        try:
            document = parse(query)
        except Exception as e:
            return ExecutionResult(errors=[e]) # type: ignore

        operation_ast = get_operation_ast(document, operation_name)

        if (
            request.method.lower() == "get"
            and operation_ast is not None
            and operation_ast.operation != OperationType.QUERY
        ):
            if show_graphiql:
                return None

            raise HttpError(
                HttpResponseNotAllowed(
                    ["POST"],
                    "Can only perform a {} operation from a POST request.".format(
                        operation_ast.operation.value
                    ),
                )
            )

        validation_errors = validate(
            schema,
            document,
            self.validation_rules,
            graphene_settings.MAX_VALIDATION_ERRORS, # type: ignore
        )

        if validation_errors:
            return ExecutionResult(data=None, errors=validation_errors)

        try:
            execute_options = {
                "root_value": self.get_root_value(request),
                "context_value": self.get_context(request),
                "variable_values": variables,
                "operation_name": operation_name,
                "middleware": self.get_middleware(request),
            }
            if self.execution_context_class:
                execute_options[
                    "execution_context_class"
                ] = self.execution_context_class

            if (
                operation_ast is not None
                and operation_ast.operation == OperationType.MUTATION
                and (
                    graphene_settings.ATOMIC_MUTATIONS is True
                    or connection.settings_dict.get("ATOMIC_MUTATIONS", False) is True
                )
            ):
                with transaction.atomic():
                    result = execute(schema, document, **execute_options)
                    if getattr(request, MUTATION_ERRORS_FLAG, False) is True:
                        transaction.set_rollback(True)
                return result

            return execute(schema, document, **execute_options)
        except Exception as e:
            return ExecutionResult(errors=[e]) # type: ignore


    @staticmethod
    def format_error(error):
        try:
            if isinstance(error, GraphQLError):
                return RkFormattedError(
                    message=error.message,
                    # locations=error.locations,
                    # path=error.path,
                    stack={**error.extensions,}, # type: ignore
                )
            else:
                return RkFormattedError(
                    message=str(error),
                    stack={"error": error},
                )
        except Exception as e:
            return {"message": str(error), "stack": {"error": str(e)}}


# class AuthGraphQLView(GraphQl):
#     def execute_graphql_request(self, request, data, query, variables, operation_name, show_graphiql=False):
#         if not request.method.lower() == "get":
#             status = check_auth_token(request.headers.get("Authorization", ""))
#             if (request.headers.get("Authorization", "") == ""):
#                 validation_errors = [GraphQLError('Authorization header is missing')]
#                 return ExecutionResult(errors=validation_errors)
#             elif (status == False):
#                 validation_errors = [GraphQLError('Authorization header has invalid token')]
#                 return ExecutionResult(errors=validation_errors)
#             else:
#                 return super().execute_graphql_request(request, data, query, variables, operation_name, show_graphiql)