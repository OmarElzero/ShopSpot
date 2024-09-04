# ShopSpot

ShopSpot is a clone of Amazon, designed to offer a similar online shopping experience. It allows users to browse and purchase products, view product details, manage their shopping cart, and complete orders. The platform supports features such as user authentication, product filtering by categories and price, customer reviews, and order tracking. This project is built using Django for the backend and React.js for the frontend, providing a robust and dynamic user interface.

## Features

- **User Authentication**: Secure login and registration for users.
- **Product Browsing**: Browse a wide range of products categorized by type.
- **Shopping Cart**: Add products to the cart and manage quantities before purchase.
- **Order Management**: Track orders from placement to delivery.
- **Product Filtering**: Filter products by categories, price, and ratings.
- **Customer Reviews**: View and add reviews to products.

## Technologies Used

- **Backend**: Django
- **Frontend**: React.js
- **Database**: sqlite3
- **API**: Django REST Framework

## Running the Project Locally

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/OmarElzero/ShopSpot.git
    cd ShopSpot
    ```

2. **Set Up Virtual Environment:**

    - **On Windows:**

        ```bash
        python -m venv venv
        venv\Scripts\activate
        ```

    - **On macOS/Linux:**

        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```

3. **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Configure Environment Variables:**

    Create a `.env` file based on `.env.example` and update it with your settings.

5. **Apply Migrations:**

    ```bash
    python manage.py migrate
    ```

6. **Create a Superuser (Optional):**

    ```bash
    python manage.py createsuperuser
    ```

7. **Run the Development Server:**

    ```bash
    python manage.py runserver
    ```

8. **Front-End Setup:**

    If you need to work on the front-end, ensure you have Node.js and npm installed. Navigate to the front-end directory and run:

    ```bash
    npm install
    npm start
    ```

9. **Access the Application:**

    Open your browser and go to `http://127.0.0.1:8000/`.

## Additional Notes

- Ensure you have any necessary API keys and credentials in your `.env` file.
- Follow specific instructions in the front-end README if there are additional setup steps.

