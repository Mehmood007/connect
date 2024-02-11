# Connect

## Description

**Connect is a Django project aimed at recreating the functionality and user experience of Facebook, providing a platform for social networking and communication. This project encompasses various features commonly found on social media platforms, including user authentication, profile creation, posting updates, connecting with friends, and more.**

## Features

- User Authentication
- Profiles
- Posting Updates



### Technologies Used

| HTML | CSS | JavaScript | Python | Django | PostgreSQL |
|------|-----|------------|--------|--------|------------|
| <img src="https://upload.wikimedia.org/wikipedia/commons/6/61/HTML5_logo_and_wordmark.svg" width="50"> | <img src="https://upload.wikimedia.org/wikipedia/commons/d/d5/CSS3_logo_and_wordmark.svg" width="50"> | <img src="https://upload.wikimedia.org/wikipedia/commons/9/99/Unofficial_JavaScript_logo_2.svg" width="50"> | <img src="https://upload.wikimedia.org/wikipedia/commons/c/c3/Python-logo-notext.svg" width="50"> | <img src="https://upload.wikimedia.org/wikipedia/commons/7/75/Django_logo.svg" width="50"> | <img src="https://wiki.postgresql.org/images/3/30/PostgreSQL_logo.3colors.120x120.png" width="50"> |



## Setup Locally
- **First clone repo locally**  
  **Run below command in terminal**  
  `git clone https://github.com/Mehmood007/connect`


- **Navigate to Directory**   
`cd connect`

- **Install Dependencies**  
  - First make sure virtual environment is activated  
  - Make sure you have postgres installed on system and running  
`pip install -r requirements.txt`

- **Setup .env**  
  - Create `.env` file inside project  
  - Look into `.env-sample` and fill `.env` accordingly  


- **Run Migrations in app directory**  
  - Make sure you have created db in postgres  
  `python manage.py makemigrations`  
  `python manage.py migrate`


- **Run Server**  
  `python manage.py runserver`