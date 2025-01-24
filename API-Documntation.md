# API Documentation

## Authentication

### Login
**URL:** `http://127.0.0.1:8000/profiles/login/`

**Method:** `POST`

**Description:** Allows users to log in to their accounts.

**Request Body:**
```json
{
  "username": "string",
  "password": "string"
}
```

**Response Example:**
```json
{
  "success": true,
  "token": "your-authentication-token"
}
```

### Logout
**URL:** `http://127.0.0.1:8000/profiles/logout/`
**Method:** `POST`
**Description:** Logs the user out and invalidates the session token.

---

```json
{
    "success": true,
    "message": "Logged out successfully"
}
```

## Customer Management

### Customer Profile
**URL:** `http://127.0.0.1:8000/profiles/profile/customer/`

- **Create (Registration)**  
  **Method:** `POST`  
  **Description:** Registers a new customer profile.
  
  **Request Body:**
```json
{
  "name": "string",
  "phone": "num",
  "email": "string",
  "address": "string",
  "username": "string",
  "password": "string"
}
```

**Response Example:**
```json
{
   "id": "num",
   "name": "string",
   "phone": "num",
   "email": "string",
   "address": "string",
   "username": "string",
   "password": "string"
    "user": "num"
}
```
  

- **View Profile**  
  **Method:** `GET`  
  **Description:** Retrieves the customer’s profile details (only the user it self or admin r super admin are allowed).
   

- **Edit Profile**  
  **Method:** `PUT`  
  **Description:** Updates an existing customer profile.
     
  **Request Body:**
```json
{
  "name": "string",
  "phone": "num",
  "email": "string",
  "address": "string",
  "username": "string",
  "password": "string"
}
```

**Response Example:**
```json
{
   "id": "num",
   "name": "string",
   "phone": "num",
   "email": "string",
   "address": "string",
   "username": "string",
   "password": "string"
    "user": "num"
}
```

- **Delete Profile**  
  **Method:** `DELETE`  
  **Description:** Deletes the customer’s profile.  

---

## Product Management

### Products
**URL:** `http://127.0.0.1:8000/categories/Categories/Products/`

- **Create Product**  
  **Method:** `POST`  
  **Description:** Adds a new product.
    **Request Body:**
```json
{
            
            "name": "string",
            "description": "string",
            "price": "string",
            "quantity": "num",
            "image": "url",
            "color": "string",
            "size": "string",
            "category": "num",
            
        }
```

**Response Example:**
```json
{
            "id": "num",
            "name": "string",
            "description": "string",
            "price": "string",
            "quantity": "num",
            "image": "url",
            "color": "string",
            "size": "string",
            "category": "num",
            "seller": "num"
        },
```


- **View Products**  
  **Method:** `GET`  
  **Description:** Retrieves the list of products or a one element(in case of one element provide the pk).  

- **Edit Product**  
  **Method:** `PUT`  
  **Description:** Updates a product's details.

    **Request Body:**
```json
{
            
            "name": "string",
            "description": "string",
            "price": "string",
            "quantity": "num",
            "image": "url",
            "color": "string",
            "size": "string",
            "category": "num",
            
        }
```

**Response Example:**
```json
{
            "id": "num",
            "name": "string",
            "description": "string",
            "price": "string",
            "quantity": "num",
            "image": "url",
            "color": "string",
            "size": "string",
            "category": "num",
            "seller": "num"
        },
```
  

- **Delete Product**  
  **Method:** `DELETE`  
  **Description:** Deletes a product.  

---

## Cart Management

### Cart Items
**URL:** `http://127.0.0.1:8000/categories/Categories/cart_items/`

- **Create Item**  
  **Method:** `POST`  
  **Description:** Adds an item to the cart.
**Request Body:**
```json
 {
            "item":"num",
            "quantity": "num"
            
        }
```

**Response Example:**
```json
{
    "id": "num",
    "date": "string",
    "quantity": "num",
    "price": "string",
    "is_ordered": "bolean",
    "item": num
}
```
 

- **View Items**  
  **Method:** `GET`  
  **Description:** Retrieves items in the cart (only for admin and user who creates this item).  

- **Edit Item**  
  **Method:** `PUT`  
  **Description:** Updates a cart item.
  **Request Body:**
```json
 {
            "item":"num",
            "quantity": "num"
            
        }
```

**Response Example:**
```json
{
    "id": "num",
    "date": "string",
    "quantity": "num",
    "price": "string",
    "is_ordered": "bolean",
    "item": "num"
}
```

- **Delete Item**  
  **Method:** `DELETE`  
  **Description:** Removes an item from the cart.  

### Cart
**URL:** `http://127.0.0.1:8000/categories/Categories/cart/`

- **just get your cart , carts made automatically** 

---

## Categories

**URL:** `http://127.0.0.1:8000/categories/Categories/category/`

- **Create Category**  
  **Method:** `POST`  
  **Description:** Adds a new category.

  **Request Body:**
```json
{
  "name": "String"
}
```

**Response Example:**
```json
{
    "id": "num",
    "name": "string"
}
```

- **View Categories**  
  **Method:** `GET`  
  **Description:** Retrieves the list of categories.  

- **Edit Category**  
  **Method:** `PUT`  
  **Description:** Updates a category's details.
    **Request Body:**
```json
{
  "name": "String"
}
```

**Response Example:**
```json
{
    "id": "num",
    "name": "string"
}
``` 

- **Delete Category**  
  **Method:** `DELETE`  
  **Description:** Deletes a category.  

---

## Order Management

### Order Items
**URL:** `http://127.0.0.1:8000/categories/Categories/order_item/`

- **Create Order Item**  
  **Method:** `POST`  
  **Description:** Adds a new order item.

   **Request Body:**
```json
 {
  "ordered_items": [ "list"
  ]
}

```

**Response Example:**
```json
 {
  "ordered_items": [ "list"
  ]
}
```

- **View Order Items**  
  **Method:** `GET`  
  **Description:** Retrieves the list of order items.  

- **Edit Order Item**  
  **Method:** `PUT`  
  **Description:** Updates an order item's details.
     **Request Body:**
```json
 {
  "ordered_items": [ "list"
  ]
}

```

**Response Example:**
```json
 {
  "ordered_items": [ "list"
  ]
}
```

- **Delete Order Item**  
  **Method:** `DELETE`  
  **Description:** Deletes an order item.  

### Orders 
**URL:** `http://127.0.0.1:8000/categories/Categories/order/`

- **View Orders**  
  **Method:** `GET`  
  **Description:** Retrieves the list of orders. Orders are created automatically.  

---

## Notes
- Ensure all requests requiring authentication include the appropriate token in the headers:  
  **Header:** `Authorization: Token <your-token>`
- Replace `http://127.0.0.1:8000` with the deployed server URL for production.
- Request and response formats may vary based on specific implementations.  
