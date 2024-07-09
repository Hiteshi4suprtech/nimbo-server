# nimboapp/schema.py

from ariadne import QueryType, MutationType, make_executable_schema, gql
from django.db import connection
from datetime import datetime

type_defs = gql("""
    type Query {
        _empty: String
    }

    type Mutation {
        registerUserWithEmail(email: String!): UserEmailRegistrationResponse!
    }

    type UserEmailRegistrationResponse {
        success: Boolean!
        message: String!
        user: User
    }

    type User {
        email: String!
        is_email_verified: Boolean!
        created_at: String!
        updated_at: String!
    }
""")

query = QueryType()
mutation = MutationType()

@mutation.field("registerUserWithEmail")
def resolve_register_user_with_email(_, info, email):
    try:
        with connection.cursor() as cursor:
            # Check if the email already exists
            cursor.execute("""
                SELECT user_id FROM users_shard WHERE email = %s
            """, [email])
            existing_user = cursor.fetchone()

            if existing_user:
                return {
                    "success": False,
                    "message": "Email already in use",
                    "user": None
                }

            # Insert new user if email does not exist
            created_at = updated_at = datetime.now().isoformat()
            cursor.execute("""
                INSERT INTO users_shard (email, is_email_verified, created_at, updated_at)
                VALUES (%s, %s, %s, %s)
                RETURNING email, is_email_verified, created_at, updated_at
            """, [email, False, created_at, updated_at])
            user = cursor.fetchone()
        
        if user:
            return {
                "success": True,
                "message": "User email registered successfully",
                "user": {
                    "email": user[0],
                    "is_email_verified": user[1],
                    "created_at": user[2],
                    "updated_at": user[3]
                }
            }
        else:
            return {
                "success": False,
                "message": "User email registration failed",
                "user": None
            }
    except Exception as e:
        return {
            "success": False,
            "message": str(e),
            "user": None
        }

schema = make_executable_schema(type_defs, query, mutation)


