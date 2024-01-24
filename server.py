from flask import Flask, request, jsonify
from blog_api.ecrivai import ArticleWriter
from flask_cors import CORS
article_writer = ArticleWriter()
print("Article writer created")

app = Flask(__name__)
app.config['OPENAI_API_KEY'] = "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"
CORS(app)
@app.route('/create_article', methods=['POST'])
def create_article():

    topic = request.json['topic']
    title = ""
    summary = ""
    title, summary, article = article_writer.create_article_openai(topic)

    result = {"title": title, "summary": summary, "article": article}

    return jsonify(result)

@app.route('/', methods=['GET'])
def test():

    article = article_writer.create_article_openai("Gold Investment", True)
    return article

if __name__ == '__main__':

    # app.run(debug=1)
    # WSGIServer(app).run()
    app.run(host='0.0.0.0', port=5000)
