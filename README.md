# WebBackEnd2
The goal of this project is to design and develop 4 scalable micro services and implement load balancer to scale the backend.

## Microservices
There are 4 microservies, each having appropriate JSON data formats, HTTP methods, URL endpoints, and HTTP status codes for each service.

- In version 1.0 of this project, its having a single SQLite database shared by all four microservices. While this architecture is viable when all services are running on a single development machine, it makes it difficult to run the services independently: either all services must remain on a single vertically-scaled server, or they must share access to a remote database server.

- While our concern in this course is primarily for the back-end, note that a microservice architecture does complicate the front-end code, requiring front-end JavaScript (or, equivalently, native code for a desktop or mobile device) to manage access to multiple services.

- While managing this complexity is, to some extent, the intent of newer back-end techniques such as GraphQL, another common approach is the Backends for Frontends (BFF) pattern, where we introduce a new back-end service which pulls together data from multiple other back-end services, exposing a single service to the front-end. In our case, the new back-end service will provide RSS feeds for the blog, contacting the other microservices as needed.

# The Project Team
## Team Members
- Shekhar Palit
- Rohan Bedarkar
- Shruti Taware
## Project Technologies
- Programming Language - Python
- Web Frame Work - Flask
- Load Balancer - Ngnix 
- RSS feeds
- DataBase - SQLite3
