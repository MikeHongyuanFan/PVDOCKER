# Product Management API

This module provides a REST API for managing loan products in the Loan Management System.

## Features

- Create, read, update, and delete products
- Associate products with applications, documents, and borrowers
- Filter products by application or borrower ID
- Search products by name
- Authentication required for all operations

## API Endpoints

All endpoints require authentication.

### List all products
```
GET /api/products/products/
```

### Create a new product
```
POST /api/products/products/
```
Required fields:
- `name`: String

Optional fields:
- `applications`: Array of application IDs
- `documents`: Array of document IDs
- `borrowers`: Array of borrower IDs

### Get a specific product
```
GET /api/products/products/{id}/
```

### Update a product
```
PUT /api/products/products/{id}/
```
or
```
PATCH /api/products/products/{id}/
```

### Delete a product
```
DELETE /api/products/products/{id}/
```

## Filtering

The API supports filtering products by:
- `application`: Filter by application ID
- `borrower`: Filter by borrower ID
- `name`: Filter by exact name match
- `name__icontains`: Filter by partial name match (case-insensitive)

Example:
```
GET /api/products/products/?application=1
GET /api/products/products/?borrower=2
GET /api/products/products/?name__icontains=mortgage
```

## Model Relationships

- One product can be linked to many applications (ManyToMany)
- One application can reference one or many products (ManyToMany)
- One product can relate to multiple documents (ManyToMany)
- One product can relate to multiple borrowers (ManyToMany)

## Implementation Details

The Product API is implemented using Django REST Framework's ModelViewSet, which provides the standard CRUD operations. The API uses token-based authentication and requires users to be authenticated for all operations.

## Testing

Unit tests are provided to verify:
- Creating, editing, and deleting a product
- Linking a product to multiple applications
- Ensuring proper ManyToMany linkage in serializer logic