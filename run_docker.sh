docker run -v $(pwd)/app:/app -t -d --name rt-ra -p 5000:5000 -e FLASK_DEBUG=1 -e FLASK_APP=/rt-ra.py rt-ra flask run --host=0.0.0.0
