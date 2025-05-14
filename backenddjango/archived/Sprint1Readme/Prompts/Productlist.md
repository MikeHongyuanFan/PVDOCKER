### ✅ Prompt for Q Chat
> Hi Q Chat, I need help implementing a full Django REST API for **Product Management** in our Loan Management System.  
> 
> ### 🧩 Purpose:
> The API should allow users to:
> - Create a product (only requires a name for now)
> - Update product information (just name editing)
> - Delete a product
> - View list of all products
>
> ### 📎 Relationship Rules:
> - One **application** can reference **one or many products**
> - One **product** can be linked to **many applications**
> - A **many-to-many** relationship between products and applications is required
> - A **product** can also relate to **multiple documents**
> - A **product** can relate to **multiple borrowers**
> - No relationship to **brokers** or **branches**
>
> ### 🛠 Requirements:
> 1. Create a `Product` model with just a `name` field.
> 2. Establish ManyToMany relationships:
>    - `applications = models.ManyToManyField(Application, related_name="products")`
>    - `documents = models.ManyToManyField(Document, related_name="products")`
>    - `borrowers = models.ManyToManyField(Borrower, related_name="products")`
> 3. Implement standard API endpoints under `/api/products/`:
>    - `GET` (list)
>    - `POST` (create with name)
>    - `PUT/PATCH` (edit name)
>    - `DELETE` (remove product)
> 4. Serializer should only require a `name` field.
> 5. Optional: Add filtering by associated application or borrower ID.
>
> ### 🔐 Auth:
> - Auth required for all operations.
>
> ### 🧪 Tests:
> - Creating, editing, and deleting a product
> - Linking a product to multiple applications
> - Ensuring proper ManyToMany linkage in serializer logic
>
> Please generate:
> - Product model
> - Product serializer
> - Product viewset (ModelViewSet is fine)
> - URL routing under `/api/products/`
> - Unit tests

