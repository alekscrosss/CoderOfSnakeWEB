# PhotoShare
"PhotoShare" is a modern REST API application built on FastAPI, designed for sharing photos among users. It provides a convenient platform for uploading, editing, deleting, and viewing photos with additional features for commenting and adding tags to images. The application supports various access levels (user, moderator, administrator), using a JWT-token based authentication system. All data, including photos and comments, are stored securely, ensuring the safety and confidentiality of user information.

## Application Usage

### Authentication

- **Registration and Login**: To use the application, registration and authentication are required. The first registered user automatically receives the status of an administrator.
- **User Roles**: Users can be assigned one of three roles: User, Moderator, Administrator. Each role provides specific levels of access to the application's features.

### Working with Photos

- **Uploading Photos**: Users can upload their photos along with a description.
- **Deleting Photos**: Users have the ability to delete their own photos.
- **Editing Descriptions**: Users can modify the descriptions of their photos.
- **Viewing Photos**: Photos can be viewed via a unique link.
- **Tags**: Each photo can have up to 5 tags, which are unique across the application.
- **Transformations**: Users can apply basic transformation operations to their photos through the Cloudinary service.
- **Creating Links for Transformed Images**: URLs and QR codes can be generated for transformed images.

### Commenting

- **Adding Comments**: Users can comment on each other's photos.
- **Editing Comments**: Users are allowed to edit their comments, but cannot delete them.
- **Deleting Comments**: Only administrators and moderators have the privilege to delete comments.
- **Timestamps**: Every comment includes the creation and last edited timestamps.


# Installation Instructions

To install and run the PhotoShare application, follow these steps:

## 1. Clone the Repository

Clone the repository from GitHub to your workspace:

#### use command: git clone https://github.com/alekscrosss/CoderOfSnakeWEB.git

## 2. Create a .env File
In the root of the project, create a .env file to store your environment variables. Insert your specific details as shown below:

APP_ENV=your_app_environment
POSTGRES_DB=your_postgres_db
POSTGRES_USER=your_postgres_user
POSTGRES_PASSWORD=your_postgres_password
POSTGRES_PORT=your_postgres_port

SQLALCHEMY_DATABASE_URL=postgresql+psycopg2://${POSTGRES_USER}:${POSTGRES_PASSWORD}@localhost:${POSTGRES_PORT}/${POSTGRES_DB}

SECRET_KEY=your_secret_key
ALGORITHM=HS256

MAIL_USERNAME=your_mail_username
MAIL_PASSWORD=your_mail_password
MAIL_FROM=your_mail_from
MAIL_PORT=your_mail_port
MAIL_SERVER=your_mail_server

REDIS_HOST=localhost
REDIS_PORT=6379

CLD_NAME=your_cloudinary_name
CLD_API_KEY=your_cloudinary_api_key
CLD_API_SECRET=your_cloudinary_api_secret

## 3. Start Docker
Ensure Docker is running on your system. You may need to start Docker from your applications menu or system settings.

## 4. Run Docker Compose
Build and start the application containers using Docker Compose:

#### in telminal use command: # docker-compose up
This command will set up all necessary services as defined in your docker-compose.yml.
## 5. Launch the Application with Uvicorn
In a new terminal session, start the FastAPI application:

#### use command: uvicorn main:app --reload
The --reload option enables auto-reloading, allowing the server to automatically restart after file changes. This is particularly useful during development.

## 6. Access the FastAPI Application
After starting the application, you can access the FastAPI UI by navigating to:

http://localhost:8000/docs
This URL provides access to the FastAPI Swagger UI, where you can test and interact with the available API endpoints.


## Conclusion

PhotoShare offers a powerful feature set for sharing and discussing photos within a convenient and secure environment. With its intuitive interface and extensive customization options, users can easily manage their content, share moments, and engage with the community. Powered by FastAPI, the application delivers high performance and efficiency, making it an outstanding choice for developing modern web applications.

# Team Members

The development and success of this project are credited to the dedicated efforts of our team:

- **Oleksandr Miestoivanchenko** - Team Lead
- **Nazar Dmitryk** - Scrum Master
- **Olha Verbova** - Developer
- **Iuliia Shyshyk** - Developer

We extend our gratitude to each team member for their hard work and commitment to making this project a reality.
