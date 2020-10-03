# IR-Engine
A simple Boolean Search Engine using Python and Flask

## Pythonanywhere
Site deployed on `pythonanywhere`: [ashishu007.pythonanywhere.com](http://ashishu007.pythonanywhere.com/)

Site deployed on `heroku`: [https://rgu-soc-bool-ir.herokuapp.com/](https://rgu-soc-bool-ir.herokuapp.com/)

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

## Heroku

Assuming you have `docker` installed and an app created on `heroku`.

0. Suppose the app created on heroku is: `rgu-soc-bool-ir`

1. Clone the repo:

    `git clone https://github.com/ashishu007/IR-Engine.git`

2. Build the docker-container:

    `docker build -t ir-eng:latest .`

3. Tag the docker-container:

    `docker tag ir-eng registry.heroku.com/rgu-soc-bool-ir/web`

4. Push the tagged container to the heroku-registry:

    `docker push registry.heroku.com/rgu-soc-bool-ir/web`

5. Release the container on heroku:

    `heroku container:release -a rgu-soc-bool-ir web`

6. Goto the browser, and type: [rgu-soc-bool-ir.herokuapp.com](https://rgu-soc-bool-ir.herokuapp.com/)

## References

* [This](https://medium.com/voice-tech-podcast/information-retrieval-using-boolean-query-in-python-e0ea9bf57f76) post on Medium.
