
### Step 1: Clone or Download the Project


cd social_network



open a terminal 



run commands: 


 python manage.py makemigrations


python manage.py migrate



Run the development server: python manage.py runserver





Then open postman to test the below mentioned apis




This document provides detailed instructions on how to use the various APIs in the social network application.

## API Endpoints

### 1. User Signup
- **URL:** `/api/users/signup/`
- **Method:** `POST`
- **Description:** Register a new user.
- **Body:**
    ```json
    {
      "username": "your_username",
      "email": "your_email@example.com",
      "password": "your_password"
    }
    ```

### 2. User Login
- **URL:** `http://localhost:8000/api/users/login/`
- **Method:** `POST`
- **Description:** Log in an existing user to obtain a JWT token.
- **Body:**
    ```json
    {
      "email": "your_email@example.com",
      "password": "your_password"
    }
    ```
- **Response:**
    ```json
    {
    "refresh":"your refresh token",
      "access": "your_jwt_token"
    }
    ```
    **Note:** Save the access token from the response. You will need it to authenticate subsequent requests.
    **Note:** If access token expires you have to use login API again to generate a new token. You will need it to authenticate subsequent requests.

### 3. Search Users
- **URL:** `http://localhost:8000/api/users/search/`
- **Method:** `GET`
- **Description:** Search users by email or username (supports partial matches on usernames).
- **Params:**
  - `query`: The search query string (email or username).
- **Headers:**
  - `Authorization: Bearer <your_jwt_token>`
- **Example in Postman:**
  - Set the request type to `GET`.
  - Enter the URL: `http://localhost:8000/api/users/search/`
  - In the Params section, add a key-value pair: `query = user@example.com` (replace with the email or username you want to search for).
  - In the Headers section, add a key-value pair: `Authorization = Bearer <your_jwt_token>`.

### 4. Send Friend Request
- **URL:** `/api/users/friend-request/send/`
- **Method:** `POST`
- **Description:** Send a friend request to another user.
- **Body:**
    ```json
    {
      "to_user_id": 2
    }
    ```
- **Headers:**
  - `Authorization: Bearer <your_jwt_token>`
- **Example in Postman:**
  - Set the request type to `POST`.
  - Enter the URL: `http://localhost:8000/api/users/friend-request/send/`
  - In the Body section, add a JSON object: `{ "to_user_id": 2 }`.
  - In the Headers section, add a key-value pair: `Authorization = Bearer <your_jwt_token>`.

### 5. List Pending Friend Requests
- **URL:** `/api/users/friend-requests/pending/`
- **Method:** `GET`
- **Description:** List all pending friend requests for the logged-in user.
- **Headers:**
  - `Authorization: Bearer <your_jwt_token>`
- **Example in Postman:**
  - Set the request type to `GET`.
  - Enter the URL: `http://localhost:8000/api/users/friend-requests/pending/`
  - In the Headers section, add a key-value pair: `Authorization = Bearer <your_jwt_token>`.
  - Remember the id of user which you want to accept or reject
  {
        "id": 13,
        "timestamp": "2024-06-07T16:08:23.705343Z",
        "from_user": 11,
        "to_user": 14
    },
  
### 6. Respond to Friend Request
- **URL:** `/api/users/friend-request/respond/`
- **Method:** `POST`
- **Description:** Accept or reject a friend request.
- **Body:**
    ```json
    {
      "request_id": 1,
      "response": "accept"
    }

     **Body:**
    ```json
    {
      "request_id": 1,
      "response": "reject"
    }
    ```
- **Headers:**
  - `Authorization: Bearer <your_jwt_token>`
- **Example in Postman:**
  - Set the request type to `POST`.
  - Enter the URL: `http://localhost:8000/api/users/friend-request/respond/`
  - In the Body section, add a JSON object: `{ "request_id": 1, "response": "accept" }`.
  - In the Headers section, add a key-value pair: `Authorization = Bearer <your_jwt_token>`.

  **Correct Usage:** Before responding to a friend request, you must first run the pending friend request API(http://localhost:8000/api/users/friend-request/pending/) to get the exact `request_id`. Then, use the `request_id` in the respond API.

  **Important:** If you want to accept or reject a friend request, you need to log in from the account to which the friend request is sent.

### 7. List Friends
- **URL:** `/api/users/friends/`
- **Method:** `GET`
- **Description:** List all friends of the logged-in user.
- **Headers:**
  - `Authorization: Bearer <your_jwt_token>`
- **Example in Postman:**
  - Set the request type to `GET`.
  - Enter the URL: `http://localhost:8000/api/users/friends/`
  - In the Headers section, add a key-value pair: `Authorization = Bearer <your_jwt_token>`.

## Important Notes

### Obtain Token
- Always obtain the JWT token by logging in (`/api/users/login/`) before making requests to protected endpoints.
- Copy the token from the login response and include it in the Authorization header for other requests.

### Sending Friend Requests
- When sending a friend request (`/api/users/friend-request/send/`), make sure to use the correct `to_user_id`.

### Responding to Friend Requests
- Before responding to a friend request (`/api/users/friend-request/respond/`), use the pending requests endpoint (`/api/users/friend-request/pending/`) to get the actual `request_id` for the friend request.
- If you want to accept or reject a friend request, you need to log in from the account to which the friend request is sent.

## Postman Collection
A Postman collection is included in the repository for fast evaluation. Import the collection into Postman to quickly test all API endpoints.

## Requirements
- Django
- Django REST framework
- Django REST framework simplejwt

See `requirements.txt` for the full list of dependencies.

## Example Workflow
1. **User Signup**
   - Endpoint: `/api/users/signup/`
   - Method: `POST`
   - Body:
     ```json
     {
       "username": "testuser",
       "email": "test@example.com",
       "password": "password123"
     }
     ```

2. **User Login**
   - Endpoint: `/api/users/login/`
   - Method: `POST`
   - Body:
     ```json
     {
       "email": "test@example.com",
       "password": "password123"
     }
     ```
   - Save the JWT token from the response.

3. **Search Users**
   - Endpoint: `/api/users/search/`
   - Method: `GET`
   - Params: `query=email or username`
   - Headers: `Authorization: Bearer <your_jwt_token>`

4. **Send Friend Request**
   - Endpoint: `/api/users/friend-request/send/`
   - Method: `POST`
   - Body:
     ```json
     {
       "to_user_id": 2
     }
     ```
   - Headers: `Authorization: Bearer <your_jwt_token>`

5. **List Pending Friend Requests**
   - Endpoint: `/api/users/friend-requests/pending/`
   - Method: `GET`
   - Headers: `Authorization: Bearer <your_jwt_token>`

6. **Respond to Friend Request**
   - Endpoint: `/api/users/friend-request/respond/`
   - Method: `POST`
   - Body:
     ```json
     {
       "request_id": 1,
       "response": "accept"
     }
     ```
   - Headers: `Authorization: Bearer <your_jwt_token>`

7. **List Friends**
   - Endpoint: `/api/users/friends/`
   - Method: `GET`
   - Headers: `Authorization: Bearer <your_jwt_token>`
