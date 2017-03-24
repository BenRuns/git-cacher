# git-cacher
This caches requests to github's api so that I don't hit their request limit as fast.
runs on google app engine

### Requirements

- Google App Engine for Python
  - Ubuntu:  [https://cloud.google.com/sdk/docs/#deb](https://cloud.google.com/sdk/docs/#deb)
  - Mac: [https://cloud.google.com/sdk/docs/#mac](https://cloud.google.com/sdk/docs/#mac)


### Setup


1. Register an Oauth application with github [here](https://github.com/settings/applications/new)

2. In the root directory create a secret.json file with the following
        {
          "github:{
            "client_id": id_from_step_1,
            "client_secret": secret_from_step_1
          }
        }
3.  Run the app

       $ dev_appserver.py app.yaml


### Deploy

    gcloud app deploy

