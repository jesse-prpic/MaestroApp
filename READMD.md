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

Flask: A lightweight web framework that simplifies the process of building web applications. It provides routing, templating, and request handling.

Flask-SQLAlchemy: An extension for Flask that adds support for SQLAlchemy, an ORM that facilitates database manipulation through Python objects rather than SQL queries.

Flask-Marshmallow: This library enables serialization and deserialization of complex data types. It makes it easy to convert SQLAlchemy models to JSON, which is essential for building APIs.

Flask-Bcrypt: Utilized for securely hashing passwords. This ensures that user passwords are stored in a way that protects against data breaches.

Flask-JWT-Extended: Provides mechanisms for implementing JWT (JSON Web Tokens) for user authentication. This ensures secure access to the API.

PostgreSQL or SQLite: Database management systems that store the application's data. PostgreSQL is often favored for its robustness and scalability, while SQLite is excellent for development and small-scale applications.

## R4
Explain the benefits and drawbacks of this app’s underlying database system.

Benefits:

Data Integrity: Ensures that relationships between tables maintain data integrity. For instance, a song cannot exist without an associated artist or genre.

Scalability: The chosen database system (like PostgreSQL) can handle large datasets and concurrent users, making it suitable for applications with a growing user base.

Advanced Querying: Supports complex queries that can efficiently retrieve information, such as fetching all songs by a particular artist or all playlists containing a specific song.



## R5
Explain the features, purpose and functionalities of the object-relational mapping system (ORM) used in this app.

## R6
Design an entity relationship diagram (ERD) for this app’s database, and explain how the relations between the diagrammed models will aid the database design. 

The ERD would include the following entities and relationships:

User: Represents users of the application. Attributes may include id, name, email, and password.
Playlist: Represents user-created playlists. Attributes may include id, name, and user_id (foreign key).
Song: Represents individual songs. Attributes may include id, title, artist_id, genre_id, and album_id.
Artist: Represents musical artists. Attributes may include id and name.
Album: Represents music albums. Attributes may include id, title, and relationships to songs.
Genre: Represents music genres. Attributes may include id and name.
Relationships:

User to Playlist: One user can have many playlists (1-to-N).
Playlist to Song: Many-to-many relationship via a join table (PlaylistSong).
Artist to Song: An artist can have multiple songs (1-to-N).
Album to Song: An album can contain multiple songs (1-to-N).
Genre to Song: A genre can be associated with multiple songs (1-to-N).
Benefits of ERD:

Visualization: Provides a clear visualization of how data entities interact, aiding in understanding the application structure.
Database Normalization: Helps identify potential redundancies and design a normalized database schema.
Facilitates Development: Guides developers during implementation by providing a reference for relationships and constraints.

## R7
Explain the implemented models and their relationships, including how the relationships aid the database implementation.

Models:

User: Contains user-related information. Each user can have multiple playlists. This one-to-many relationship allows efficient organization of user-generated content.
Album: Represents music albums and includes a relationship with songs. This allows songs to be grouped under their respective albums for easy retrieval.
Artist: Each artist can have multiple songs associated with them, which simplifies queries related to artist discographies.
Genre: Similar to artist, genres can link to multiple songs, aiding in organization and retrieval based on music style.
Song: Central to the application, linking to artists, genres, and albums. This model facilitates complex queries and relations.
Playlist: Connects users to their song collections, allowing for flexible playlist creation and modification.
How Relationships Aid Implementation:

Efficiency: Relationships enable efficient data retrieval. For example, fetching all songs from a particular artist becomes straightforward due to the established foreign key relationships.
Data Integrity: Relationships enforce referential integrity. If an artist is deleted, any associated songs can be automatically managed (e.g., set to NULL or deleted).
Complex Queries: Relationships facilitate complex queries involving joins, enabling the app to deliver rich data interactions, like retrieving all playlists containing a specific song.

## R8
Explain how to use this application’s API endpoints. Each endpoint should be explained, including the following data for each endpoint:

HTTP verb
Path or route
Any required body or header data
Response

