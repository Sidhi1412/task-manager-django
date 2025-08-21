# Personal Task Management API (Django + DRF + Graphene)

Lightweight backend with REST + GraphQL (queries + mutations). Auth via DRF tokens.
GraphQL access is restricted behind a custom authenticated GraphQL view.

## Quickstart

```bash
python3 -m venv venv
source venv/bin/activate  # Windows: .\venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## REST: Get Token
```http
POST /api/get-token/
{ "username": "<user>", "password": "<pass>" }
```
Use header `Authorization: Token <token>` for all subsequent calls.

## REST Endpoints
- GET  /api/tasks/
- POST /api/tasks/            # { "title": "My task", "status": "PENDING" }
- GET  /api/tasks/<id>/
- PUT  /api/tasks/<id>/       # { "title": "New", "status": "COMPLETED" }
- DELETE /api/tasks/<id>/

## GraphQL
Endpoint: `/graphql/` (requires `Authorization: Token <token>` header)

### Query
```graphql
query {
  allTasks {
    id
    title
    status
    createdAt
  }
}
```

### Mutations (DRF serializer reused)
```graphql
mutation {
  createTask(title: "From GQL", status: "PENDING") {
    ok
    errors
    task { id title status }
  }
}

mutation {
  updateTask(id: 1, status: "COMPLETED") {
    ok
    errors
    task { id title status }
  }
}

mutation {
  deleteTask(id: 1) { ok }
}
```

## Notes
- Valid `status` values: `PENDING | IN_PROGRESS | COMPLETED`
- DB: SQLite by default; swap `DATABASES` in `settings.py` for Postgres if desired.
- Bonus: Mutations implemented using the DRF `TaskSerializer` for validation.
