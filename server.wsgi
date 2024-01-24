from flask import Flask, request, jsonify
from ecrivai.add_blog import ArticleWriter
from flup.server.fcgi import WSGIServer
article_writer = ArticleWriter()
print("Article writer created")
import os
import numpy as np

app = Flask(__name__)
app.config['OPENAI_API_KEY'] = "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"
@app.route('/create_article', methods=['POST'])
def create_article():

    topic = request.json['topic']

    article = article_writer.create_article_openai(topic)

    result = {'article': article}

    return jsonify(result)

if __name__ == '__main__':

    # app.run(debug=1)
    WSGIServer(app).run()
    # app.run(host='0.0.0.0', port=5000)
