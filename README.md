# IR-Engine
A simple Boolean Search Engine using Python and Flask

## Pythonanywhere
Site deployed on `pythonanywhere`: [ashishu007.pythonanywhere.com](http://ashishu007.pythonanywhere.com/)

## Docker
To run the application using `docker`, use the following steps:

1. Pull the image from docker-hub using:

    `docker pull ashishu007/rgu-soc-boolean-ir:latest`

2. Run the docker image:

    `docker run -d -p 5000:5000 ashishu007/rgu-soc-boolean-ir:latest`

3. Goto [`localhost:5000`](http://localhost:5000) in your browser

To stop the running image, follow these steps:

1. List the active images using:

    `docker ps`

2. Copy the unique `CONTAINER ID` (let's say, _containerid_) for the image `ashishu007/rgu-soc-boolean-ir`

3. Run:

    `docker stop containerid`

It assumes, you've docker installed.

## References

* [This](https://medium.com/voice-tech-podcast/information-retrieval-using-boolean-query-in-python-e0ea9bf57f76) post on Medium.
