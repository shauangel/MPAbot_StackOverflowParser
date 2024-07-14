#!/usr/bin/env python
import os
from flasgger import Swagger
from flask import Flask, jsonify, request
from models import stack_overflow_parser, outer_search
from models import db_manager as db

app = Flask(__name__)
app.config['SWAGGER'] = {
    "title": "Stack Overflow Parsing Service",
    "description": "API for Stack Overflow data collection & retrieval",
    "version": "2.0",
    "termsOfService": "",
    "hide_top_bar": True
}
swagger = Swagger(app=app, template_file="swagger_doc.yml")


@app.route('/hello', methods=['GET'])
def hello():
    return jsonify({"result": "hello"})


# search only, return urls
@app.route('/search', methods=['GET'])
def search():
    # Step 1: Get parameters
    keywords = request.values.get('keywords')
    page = int(request.values.get('page'))
    result_num = int(request.values.get('num'))

    try:
        # Step 2: Start searching
        result = outer_search.outer_search(keywords=keywords.split(';'),
                                           result_num=int(result_num),
                                           page_num=int(page))
        response = {"result": result}
    except Exception as e:
        response = {"error": e.__class__.__name__ + " : " + e.args[0]}
    return jsonify(response)


@app.route('/retrieve', methods=['POST'])
def retrieve():
    data = request.get_json()
    try:
        # Step 1: Search webpages by Google
        result = data["links"]

        # Step 2: Generate Stack Overflow objects
        so_parser = stack_overflow_parser.StackData(result)

        # Step 3: Check if posts is in database
        id_list = so_parser.get_ids()
        records = db.query_post_by_id(id_list)

        # Step 4: Check if the parser needs to get more data
        if len(records) == len(id_list):
            # Step 5-1: If all the websites are collected, return records
            response = records
        else:
            # Step 5-2: Modify data, update new ids & links needs to be parse
            for r in records:
                id_list.remove(r['question']['id'])
            so_parser.set_ids(id_list)

            # Step 6: Parse data from stack exchange API
            so_parser.start_parsing()
            new_parsed = so_parser.get_results()

            # Step 7: Insert new posts data
            insert_id = db.insert_posts(new_parsed)
            # print(insert_id)

            # Step 8: return result
            response = records + new_parsed
            for r in response:
                try:
                    r.pop("_id")
                except:
                    continue

    except Exception as e:
        response = {"error": e.__class__.__name__ + " : " + e.args[0]}
    return jsonify(response)


if __name__ == "__main__":
    print("Welcome to SO service system~~")
    app.run(host='0.0.0.0', port=os.environ.get("FLASK_SERVER_PORT", 8001), debug=True)
