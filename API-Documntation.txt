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
  "token": "your-authentication-token"
}
```

### Logout
**URL:** `http://127.0.0.1:8000/profiles/logout/`
**Method:** `POST`
**Description:** Logs the user out and invalidates the session token.

---

## Customer Management

### Customer Profile
**URL:** `http://127.0.0.1:8000/profiles/profile/customer/`

- **Create (Registration)**  
  **Method:** `POST`  
  **Description:** Registers a new customer profile.  

- **View Profile**  
  **Method:** `GET`  
  **Description:** Retrieves the customer’s profile details.  

- **Edit Profile**  
  **Method:** `PUT`  
  **Description:** Updates an existing customer profile.  

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

- **View Products**  
  **Method:** `GET`  
  **Description:** Retrieves the list of products.  

- **Edit Product**  
  **Method:** `PUT`  
  **Description:** Updates a product's details.  

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

- **View Items**  
  **Method:** `GET`  
  **Description:** Retrieves items in the cart.  

- **Edit Item**  
  **Method:** `PUT`  
  **Description:** Updates a cart item.  

- **Delete Item**  
  **Method:** `DELETE`  
  **Description:** Removes an item from the cart.  

### Cart
**URL:** `http://127.0.0.1:8000/categories/Categories/cart/`

- **CRUD operations**

---

## Categories

**URL:** `http://127.0.0.1:8000/categories/Categories/category/`

- **Create Category**  
  **Method:** `POST`  
  **Description:** Adds a new category.  

- **View Categories**  
  **Method:** `GET`  
  **Description:** Retrieves the list of categories.  

- **Edit Category**  
  **Method:** `PUT`  
  **Description:** Updates a category's details.  

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

- **View Order Items**  
  **Method:** `GET`  
  **Description:** Retrieves the list of order items.  

- **Edit Order Item**  
  **Method:** `PUT`  
  **Description:** Updates an order item's details.  

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
  **Header:** `Authorization: Bearer <your-token>`
- Replace `http://127.0.0.1:8000` with the deployed server URL for production.
- Request and response formats may vary based on specific implementations.  
