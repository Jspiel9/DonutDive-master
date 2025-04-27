Website created with Django for a school project, old user auth key and email that are locked so there are no security breaches on my end and they can be out there to show how it works. 

Running a Server in Django
1
2
3
To run a server in Django, you need to follow a few steps to set up your environment, create a project, and start the development server. Here is a step-by-step guide:

Setting Up the Environment

Create a Virtual Environment: It is recommended to use a virtual environment to manage dependencies for your Django project. Run the following command to create a virtual environment:

python3 -m venv venv
Install Django: Once the virtual environment is activated, install Django using pip:

pip install django
Creating a Django Project

Start a New Project: Use the django-admin command to create a new project. Replace projectName with your desired project name:

django-admin startproject projectName
Running the Development Server

Run the Server: Use the manage.py script to start the development server:

python manage.py runserver
Additional Information

Project Structure: When you create a Django project, it includes several important files such as manage.py, settings.py, urls.py, wsgi.py, and asgi.py. These files help manage the project settings, URL routing, and server configurations
1
.

Automatic Reloading: The development server automatically reloads when you make changes to your code, so you don't need to restart the server manually
2
.

By following these steps, you can quickly set up and run a Django server for your web application development. This setup allows you to develop and test your application locally before deploying it to a production environment
3
.

Learn more
1
geeksforgeeks.org
2
docs.djangoproject.com
3
w3schools.com
