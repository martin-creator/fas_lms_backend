# Future African Scientist Community Hub
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.12%2B-brightgreen)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-4.2%2B-brightgreen)](https://www.djangoproject.com/)


  <img src="https://techstack-generator.vercel.app/python-icon.svg" alt="icon" width="40" height="40" /> <img src="https://techstack-generator.vercel.app/django-icon.svg" alt="icon" width="40" height="40" />

Welcome to the Django LMS project! This project aims to provide a comprehensive learning management system with features like user profiles, messaging, notifications, job listings, groups, followers, events, courses, connections, companies, and certifications.

## Project Under Development....🥶🥱😴
<img src="https://github.com/AbdullahBakir97/AbdullahBakir97/blob/main/assets/tech.gif" alt="Tech" width="100"> 

**Note**: This project is currently under development. Stay tuned for upcoming features and enhancements.

# Overview

Django LMS is a sophisticated learning management system crafted using Django, a high-level Python web framework. LMS platform is meticulously engineered to provide users with a seamless experience in managing various aspects of their educational and professional journeys. Whether you're an educator, a student, or a professional seeking growth opportunities, Django LMS offers a comprehensive suite of features to meet your needs.

## Features
![scrnli_13_06_2024_22-49-11](https://github.com/AbdullahBakir97/Django--LMS--Learning-Management-System/assets/127149804/fd107a30-91ef-435b-9ef7-fcf41ba51ec5)
![scrnli_13_06_2024_22-49-51](https://github.com/AbdullahBakir97/Django--LMS--Learning-Management-System/assets/127149804/5767e11a-c74e-49f6-8cfb-ae59face77d0)
![myapp_models](https://github.com/martin-creator/fas_lms_backend/assets/127149804/2b150654-52f6-48a7-915a-39b02c218e88)


### User Profiles
- **👤 Detailed Profiles**: Users can create comprehensive profiles showcasing their skills, experiences, and endorsements.
- **✏️ Customizable**: Personalize your profile to highlight your unique strengths and achievements.
- **🤝 Networking**: Connect with other users and expand your professional network effortlessly.

### Messaging and Notifications
- **💬 Real-time Communication**: Seamlessly communicate with other users through our messaging system.
- **🔔 Instant Notifications**: Stay informed about important updates, messages, and activities with our robust notification system.

### Job Listings and Applications
- **💼 Career Opportunities**: Explore a wide range of job listings tailored to your skills and preferences.
- **📝 Efficient Applications**: Apply for jobs directly through our platform and track your application status effortlessly.

### Group Management
- **👥 Create and Join Groups**: Form communities based on shared interests, goals, or affiliations.
- **🤝 Collaboration**: Collaborate with group members on projects, discussions, and events.

### Follower System
- **📈 Build Your Network**: Grow your network by following other users and staying updated on their activities.
- **💬 Engagement**: Interact with followers through posts, comments, and shared content.

### Events Management
- **📅 Organize Events**: Plan and manage events such as workshops, webinars, and conferences seamlessly.
- **📊 Attendance Tracking**: Keep track of event attendance and engagement effortlessly.

### Course Management
- **🎓 Wide Range of Courses**: Enroll in a diverse selection of courses spanning various topics and disciplines.
- **📈 Track Progress**: Monitor your course progress and achievements as you work towards completion.

### Connection Requests and Recommendations
- **🤝 Expand Your Network**: Send connection requests to other users and expand your professional circle.
- **👍 Recommendations**: Receive and provide recommendations to enhance your professional credibility.

### Company Profiles and Updates
- **🏢 Company Profiles**: Explore detailed profiles of companies, including information about their culture, mission, and career opportunities.
- **📰 Stay Updated**: Receive updates and announcements from companies you follow, keeping you informed about new developments and job openings.

### Certification Management
- **📜 Manage Certifications**: Keep track of your certifications, including issue dates, expiration dates, and related courses or jobs.
- **🔍 Credential Verification**: Verify the authenticity of certifications and share them with potential employers or collaborators.


## Setup Instructions

To set up this project locally, follow these steps:

1. **Clone the repository:**

    ```bash
    git clone https://github.com/martin-creator/fas_lms_backend.git
    cd fas_lms_backend
    ```

2. **Create a virtual environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Apply migrations:**

    ```bash
    python manage.py migrate
    ```

5. **Create a superuser:**

    ```bash
    python manage.py createsuperuser
    ```

6. **Run the development server:**

    ```bash
    python manage.py runserver
    ```

7. **Access the application:**

    Open your web browser and go to [http://localhost:8000](http://localhost:8000)




# Contributing
Contributions are welcome! Please read our [contributing guidelines](CONTRIBUTING.md) for more information.

# License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.


# Generate database diagram

  ```bash
  python manage.py graph_models -a -o myapp_models.png
  ```
  
---

Python script that offers two command options: one to generate a high-level textual representation and another to generate a UML diagram using `graphviz`. The script will save the results in separate files.


### Usage Instructions:


3. **Run the script with the desired command**:

To generate a textual representation:

 ```bash
 python model_inspector.py text
 ```

To generate a UML diagram:

 ```bash
 python model_inspector.py uml
 ```

The script will:
- Traverse your Django apps and find the model files.
- Parse the models to extract relationships.
- Generate a high-level textual representation and save it as `models_representation.md` when the `text` command is used.
- Generate a UML diagram and save it as `uml_diagram.png` when the `uml` command is used.


## Docker commands

[cheat sheet](https://www.geeksforgeeks.org/docker-cheat-sheet/)

- Build the image:

  ```bash
  docker buildx build -t fas_lms_backend .
  ```

  - Run the container:

  ```bash
    docker run -p 8000:8000 fas_lms_backend
    ```

- Run services with docker-compose:

```bash

docker compose up
```

```bash
 docker-compose up --build

```

## Central Monitoring Dashboard

- Visit: http://localhost:3000


<!-- 9e5e208376cc1c4b8c6c95f5edeadf87d435a007 -->
