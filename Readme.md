# Sample code

Flask app using a sqlite DB store. For serious use please use Postgres not sqlite. Can be queried and populated with curl.

The data in this example is *horrible*. Of the 1000 sample input lines, only 4 are valid.
For instance: Run this grep looking for creative-size:

'
$ grep creative impressions-shortlist| wc -l                                                                                     
4
'

I do not feel comfortable furthering this task or writing tests when the sample data is this
poor, because I do not know if I have misunderstood the task or if I am even working with the correct data

## To run

* pip install -r requirements.txt
* FLASK_DEBUG=1 FLASK_APP=web.py flask run

## To insert data

* python populate.py

### To use manually

* curl -X POST -H "Content-Type: application/json" -d '{"headers":{"Referer": "333"}, "date":"2015-06-13 09:19:58", "creative_size": "60x600" }'   http://127.0.0.1:5000/new_data
* curl http://127.0.0.1:5000/history
* curl http://127.0.0.1:5000/creative_sizes
