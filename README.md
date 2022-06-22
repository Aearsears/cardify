# Cardify

Turn notes into flashcards, in a flash! This is the backend for the cardify website.

The Django backend is deployed on Heroku using Docker. Due to Heroku restrictions, I use streamlit.io's services to generate the question and answer pairs using AI. I also use railway.app to host the Redis cache and message broker. WebSockets is used to notify the user when the Q&A have finished creating.

### Backend Technologies

-   Python 3
-   Django
-   GraphQL
-   WebSockets
-   PostgreSQL
-   Redis
-   Docker

## Notes

Deploy a ASGI application server to use WebSockets.
