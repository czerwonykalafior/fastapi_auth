# fastapi_auth

In this repository I'm trying to gather different kinds of authentication and authorization alog with working examples.
Eah example is in separate branch.

## [Official FastAPI](https://github.com/czerwonykalafior/fastapi_auth/tree/official_docs)
[official_docs](https://fastapi.tiangolo.com/tutorial/security/) 

From what I understand so far, documentation is showing how to implement authentication provider by using OAuth2. 
Authentication part can be used inside the API itself but authorization with scopes needs modifications. Here user is
giving himself the privilege (check [permission vs privilege vs scope](https://auth0.com/blog/permissions-privileges-and-scopes/)) 
to the resource. I want the permissions to exist in the system and privileges are assigned to users by admins.

## Using scopes as permissions
Reusing scope approach from official docs but tweaking it so that scopes are hardcoded to users in the system.


## Keyclock - https://github.com/code-specialist/fastapi-keycloak


## RBAC - https://github.com/casbin/pycasbin

