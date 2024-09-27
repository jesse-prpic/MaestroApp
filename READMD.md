# MaestroApp

## R1
Explain the problem that this app will solve, and explain how this app solves or addresses the problem.

Problem: With the fast pace digital age, it can be difficult to keep track of your music collection with multiple scattered playlists. This app addresses the need for an organised music management system where users can manage their music collections. 
It allows users to create playlists, manage songs, and track various music-related entities like artists, albums and genres.

Solution: The app provides a centralized platform where users can:

Create Playlists: 
Users can easily create and manage multiple playlists.

Organize Music: 
By associating songs with artists, albums, and genres, users can explore their music collections in an organized manner.

User Authentication: 
Users can register, log in, and maintain their personal collections securely using JWT (JSON Web Tokens) for authentication.

CRUD Operations: 
The API allows users to perform CRUD operations on songs, playlists, artists, albums, and genres through a clear and consistent interface.

## R2
Describe the way tasks are allocated and tracked in your project.

Allocation: Tasks in this project are allocated by defining specific controllers for each entity, these entities being users, playlists, songs, albums, artists. Each controller handles routes related to its entity, streamlining development and maintenance.

Tracking: Progress and issues are tracked using a version control, project management and logging system.

Version Control: Git is used for tracking changes in the codebase, allowing developers to collaborate effectively and manage code revisions.

Project Management Tools: Tools like Trello, Jira, or Asana can be used to track task progress, assign tasks, and prioritize development efforts.

Logging: Implementing logging throughout the application allows developers to monitor the flow of data and identify issues or bottlenecks in real-time.


## R3
List and explain the third-party services, packages and dependencies used in this app.

Throughout the project there has been multiple third_party services, packages and descrepencies that work to build the framework to hashing passwords.

Flask: A micro web framework for building web applications.
Flask-SQLAlchemy: An ORM that simplifies database interactions.
Flask-Marshmallow: For serializing and deserializing complex data types.
Flask-JWT-Extended: For implementing JSON Web Tokens for authentication.
bcrypt: For hashing passwords.
psycopg2: PostgreSQL database adapter for Python.
SQLAlchemy: An SQL toolkit and ORM for Python.

## R4
Explain the benefits and drawbacks of this app’s underlying database system.

## R5
Explain the features, purpose and functionalities of the object-relational mapping system (ORM) used in this app.

## R6
Design an entity relationship diagram (ERD) for this app’s database, and explain how the relations between the diagrammed models will aid the database design. 

This should focus on the database design BEFORE coding has begun, eg. during the project planning or design phase.

## R7
Explain the implemented models and their relationships, including how the relationships aid the database implementation.

This should focus on the database implementation AFTER coding has begun, eg. during the project development phase.

## R8
Explain how to use this application’s API endpoints. Each endpoint should be explained, including the following data for each endpoint:

HTTP verb
Path or route
Any required body or header data
Response


<!-- Framework of app -->
