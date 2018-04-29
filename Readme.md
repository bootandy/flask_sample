# A simple Flask app. With tests.

# To run:
 * pip install -r requirements.txt
 * FLASK_DEBUG=1 FLASK_APP=web.py flask run

# To run tests:
    py.test tests.py

## To use:
 * curl -X POST -H "Content-Type: application/json" -d '{"content": "sdfsad"}'   http://127.0.0.1:5000/documents/nw
 * curl http://127.0.0.1:5000/documents

 Note: to curl the url /documents/$NAME/$TIME the space in $TIME needs to be replaced with the url enocded
space: %20
