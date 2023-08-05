This is the official [python](https://python.org/) client for [Dr. Ashtetepe](https://drhttp.com/) service.


DrHTTP let's you record two types of requests :

 - Inbound : requests that are performed by clients of your server (eg. API calls from a mobile app)
 - Outbound (optional) : requests that are performed by your server (eg. API call to third parties)

Note: You need to configure inbound request recording to have outbound request recording working.

# Installation

Install package with `pip` (or any compatible package manager) :
```
pip install drhttp
```

# Usage for [Django](https://www.djangoproject.com/)

[An integraion example is provided here](https://bitbucket.org/drhttp/drhttp-python/src/master/examples/django/)

## Request recording

### Inbound request recording

You will need an `api_key` that can be generated [here](https://drhttp.com/).

This recording is done via a wsgi middleware. You can configure it in `wsgi.py`:

```python
application = ... # get your application from existing code

import drhttp
application = drhttp.WSGIMiddleware(app=application,
                                    dsn="https://<api_key>@api.drhttp.com",
                                    identify=lambda headers: headers.get('User'))
```

`identify` function in `drhttp.WSGIMiddleware()` is *optional*. It allows the identification of the user issuing the inbound request. You'll be able to filter requests based on this field in the web interface.

*Note: Device identification is not available yet in the python library*

### Outbound request recording

*Note: Outbound request recording is not available yet in the python library*

# Usage for [Flask](https://www.djangoproject.com/)

[An integraion example is provided here](https://bitbucket.org/drhttp/drhttp-python/src/master/examples/flask/)

## Request recording

### Inbound request recording

You will need an `api_key` that can be generated [here](https://drhttp.com/).

This recording is done via a wsgi middleware. You may need to change some code in your flask app file.
The goal is to encapsulate the wsgi app in the drhttp middleware. As `drhttp.WSGIMiddleware()` returns a wsgi application (not a full flask application) it can't be run by flask cli, you need a wsgi application server like `werkzeug/gunicorn/uwsgi`.

```python
...
app = Flask(__name__)
...

if __name__ == '__main__':
    import drhttp
    from werkzeug.serving import run_simple
    app = drhttp.WSGIMiddleware(app=app,
                                dsn="https://<api_key>@api.drhttp.com",
                                identify=lambda headers: headers.get('User'))

    run_simple('0.0.0.0', 80, app)
```

`identify` function in `drhttp.WSGIMiddleware()` is *optional*. It allows the identification of the user issuing the inbound request. You'll be able to filter requests based on this field in the web interface.

*Note: Device identification is not available yet in the python library*

### Outbound request recording

*Note: Outbound request recording is not available yet in the python library*

# Troubleshooting

Please [report any issue](https://bitbucket.org/drhttp/drhttp-python/issues/new) you encounter concerning documentation or implementation. This is very much appreciated.