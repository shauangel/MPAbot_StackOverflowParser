import json
import requests
import random

so_parser_url = "http://localhost"


if __name__ == "__main__":
    with open("samples.json", "r", encoding="utf-8") as file:
        questions = json.load(file)
    file.close()

    rand_q = {}
    for cat in questions:
        print(">> Category: " + cat)
        for x in range(3 if len(questions[cat]) > 3 else len(questions[cat])):
            q = questions[cat][len(questions[cat]) - x - 1]
            print(q)
            # Search questions
            search_requests = so_parser_url + f"/search?keywords=python;{q}&page=0&num=10"
            links = requests.get(url=search_requests).json()
            print(links)

            # Parse question
            req = {"links": links['result']}
            retrieve_url = so_parser_url + "/retrieve"
            resp = requests.post(url=retrieve_url, json=req)


    """
        # Random sampling
        rand_s = random.sample(questions[cat], 3 if len(questions[cat]) >= 3 else len(questions[cat]))
        rand_q[cat] = rand_s
    with open("samples.json", 'w', encoding='utf-8') as file:
        json.dump(fp=file, obj=rand_q)
    file.close()
    """




