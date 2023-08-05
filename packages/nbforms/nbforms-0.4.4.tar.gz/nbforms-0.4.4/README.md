# nbforms

[![Documentation Status](https://readthedocs.org/projects/nbforms/badge/?version=latest)](https://nbforms.readthedocs.io/en/latest/?badge=latest)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/chrispyles/nbforms/master?filepath=demo%2Fdemo.ipynb)

nbforms is a Python package designed to allow forms to be submitted by users such that the data they submit is immediately available for use in the notebook by the entire group. This is accomplished using ipywidgets and a Heroku-deployable Sinatra webapp, [nbforms-server](https://github.com/chrispyles/nbforms-server).

## Installation

To install the Python package, use pip:

```
pip install nbforms
```

## Deployment

### Server

Before using nbforms in a notebook, you must deploy a webapp to Heroku which will collect and organize the responses. If you plan to have multiple notebooks, you only need one server, as you can provide a notebook identifier in the config files that will distinguish responses.

To deploy the webapp, click the deploy button in the [nbforms-server README](https://github.com/chrispyles/nbforms-server).

### Config File

nbforms requires a JSON-formatted config file to set up the `Notebook` class. The default path that `Notebook` checks is `./nbforms_config.json`, although you can pass a custom path to the `Notebook` constructor. The structure of the config file is very specific; it contains the information that the notebook needs to create widgets and send requests. The structure of this file is:

```python
{
    "server_url": "",             # URL to your Heroku app

    "notebook": "",               # an ID to collect responses

    "auth": "",                   # indicates auth provider, defaults to nbforms

    "questions": [{               # questions to ask, a list of dicts

      "identifier": "",           # a question identifer, should be unique within
                                  # this notebook

      "type": "",                 # question type; can be one of:
                                  #   multiplechoice, checkbox, text, paragraph

      "question": "",             # the question text

      "options": [                # options from which to choose if type is 
        ...                       # multiplechoice or checkbox
      ],
      "placeholder": ""           # placeholder for textbox if type is text or
                                  # paragraph
    }, 
    ...                           # more question dictionaries
  ]
}
```

The `server_url` key should be the URL to your Heroku-deployed nbforms-server, e.g. `https://my-nbforms-server.herokuapp.com`. The `notebook` key should be some string or number to identify the notebook that you're deploying. This is used to keep the notebook responses distinguished on the server. The `auth` key is used to indicate which auth provider you would like to use. _Currently, we only offer Google OAuth (`google`). If you do not want to use Google, leave this key out of the config file and the default nbforms auth will be used. Finally, the `questions` key should be a list of dictionaries that define the information for your questions.

Questions can have one of four types: `multiplechoice`, `checkbox`, `text`, or `paragraph`. The `type` key in the question is used to create the widget. If you have a `multiplechoice` or `checkbox`, you must provide a list of options as the `options` key. For `text` and `paragraph` responses, you can provide an optional `placeholder` key which will replace the default placeholder.

There is a sample config file at [`demo/nbforms_config.json`](demo/nbforms_config.json). Each nbforms-server comes with a page that will generate a config file for you. The config generator for the demo server can be found [here](https://nbforms-demo-server.herokuapp.com/config_generator.html).

## Usage

### Import and Instantiate

To use the nbforms, you must first import it and create a `Notebook` instance. This will load the config file (defaulting to look at `./nbforms_config.json`) and ask the user to input a username and a password. If the username already exists on the server, the password will be checked and an API key will be generated, to be stored in the `Notebook` class. If it does not exist, a new user will be created, and an API key generated. If the user _does_ exist but an incorrect password is provided, the cell will error.

```python
import nbforms
form = nbforms.Notebook()
```

If you elect to use a 3rd party auth provider (indicated in the config file), then the cell above will instead provide a link to that provider's login page. Once the user logs in, they will be redirected back to the nbforms server and given an API key, which they will be asked to enter in the notebook.

### Collecting Responses

To collect the responses for a question, insert a cell that calls the `Notebook.ask` function on the **identifier** of the question. For example, if I had a question `q1`, I would call

```python
form.ask("q1")
```

This will output the widget and a "Submit" button that, when clicked, will send an HTTP POST request to your nbforms server with the student's API key, notebook ID, question identifier, and response to be stored on the server.

`Notebook.ask` can accept multiple questions; for example, `form.ask("q1", "q3")` would display a widget with `q1` and `q3` as its tabs. Passing no arguments to `Notebook.ask` will display all of the questions.

### Retrieving Data

nbforms allows you to get your data from the server and collect it into either a datascience `Table` or a pandas `DataFrame`. To retrieve the responses from the server, use `Notebook.to_table` or `Notebook.to_df`; the optional `user_hashes` argument (default `False`) indicates whether or not to include a column with the hashes username.

```python
# datascience Table
form.to_table("q1", "q2", ...)

# pandas DataFrame
form.to_df("q1", "q3", ..., user_hashes=True)
```

### Taking Attendance

nbforms can be used to track attendance. All attendance requests are logged and instructors have the ability to run rake tasks that will open and close the attendance form. If a student submits when the attendance is not open, their submission will indicate that the form was closed when they submitted. If it is open, this will be reflected in their submission. If a student submits attendance for a notebook when it is open and then resubmits after it is closed again, the submission when the notebook was open will not be overwritten.

To open the attendance submissions, run `rake attendance:open[NOTEBOOK_ID]` on the heroku add. Simiarly, to close it, run `rake attendance:close[NOTEBOOK_ID]`. To generate a CSV of the submissions for a particular notebook, run `rake attendance:report[NOTEBOOK_ID]`. In all of these, replace `NOTEBOOK_ID` with the ID you provided for the notebook in the config file.

To take attendance in the notebook, use `Notebook.take_attendance`:

```python
form.take_attendance()
```

The default behavior of nbforms is not to notify students if they submit when the form is closed. `Notebook.take_attendance` will only error if the submission was not recorded successfully.

## Database Maintenance

There is not much database maintance that can be done, but you can optionally delete all responses on the server by running `rake clear` on your Heroku app.

## Notes

### Setting Up Google OAuth

To use Google OAuth, you need to get set up a GCP project with OAuth and use the [Heroku dashboard](https://devcenter.heroku.com/articles/config-vars#using-the-heroku-dashboard) to set up the necessary environment variables. You should set `GOOGLE_KEY` to your client ID and `GOOGLE_SECRET` to your client secret.
