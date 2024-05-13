#!/usr/bin/env python
import os
from flasgger import Swagger, swag_from
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


# search only, return urls
@app.route('/search', methods=['POST'])
def search():
    data = request.get_json()
    try:
        result = outer_search.outer_search(keywords=data["keywords"],
                                           result_num=data["result_num"],
                                           page_num=data["page_num"])
        response = {"result": result}
    except Exception as e:
        response = {"error": e.__class__.__name__ + " : " + e.args[0]}
    return jsonify(response)


@app.route('/retrieve', methods=['POST'])
def retrieve():
    data = request.get_json()
    try:
        result = outer_search.outer_search(keywords=data["keywords"],
                                           result_num=data["result_num"],
                                           page_num=data["page_num"])
        # initialize SO parser
        so_parser = stack_overflow_parser.StackData(result)
        # check if record exists
        # id_list = so_parser.get_ids()
        # records = db.query_post_cache_by_id(id_list)
        # for r in records:
        #     if r["question"]["id"] in id_list:
        #         id_list.remove(r["question"]["id"])
        so_parser.start_parsing()
        response = so_parser.get_results()
    except Exception as e:
        response = {"error": e.__class__.__name__ + " : " + e.args[0]}
    return jsonify(response)


if __name__ == "__main__":
    print("Welcome to SO service system~~")
    app.run(host='0.0.0.0', port=os.environ.get("FLASK_SERVER_PORT", 9090), debug=True)
