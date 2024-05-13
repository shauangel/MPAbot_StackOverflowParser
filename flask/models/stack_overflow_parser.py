# Stack Overflow Parser
import requests
from urllib.parse import urlparse, unquote
from pathlib import PurePosixPath
from bs4 import BeautifulSoup
import json
from datetime import datetime


class StackData:

    # Constants & URL
    STACK_EXCHANGE_API = "https://api.stackexchange.com/2.3"
    MAX_PAGE = 25

    # initialize attributes
    def __init__(self, urls=[]):
        # collect ids
        # self.ids = [PurePosixPath(urlparse(unquote(p)).path).parts[2] for p in urls]
        self.__ids = []
        for url in urls:
            # extract ids from urls
            try:
                id = PurePosixPath(urlparse(unquote(url)).path).parts[2]
                self.__ids.append(str(int(id)))
            # ignore invalid url
            except ValueError:
                continue
        # dict of id & link
        self.__links = {k: v for (k, v) in zip(self.__ids, urls)}
        # store parsed data
        self.__results = []
        self.__questions = []

    # start fetching website content
    def start_parsing(self):
        self.get_questions()
        self.get_answers()

    # Construct request API URL
    def get_api_url(self, page, answers):
        ids = ";".join(self.__ids)
        params = "&site=stackoverflow&filter=withbody"
        if answers:
            return self.STACK_EXCHANGE_API + "/questions/" + ids + "/answers?page=" + page + params
        return self.STACK_EXCHANGE_API + "/questions/" + ids + "?page=" + page + params

    # Send requests to Stack Exchange API
    def get_stackexchange_response(self, is_answers):
        # is_answer: True -> for answer posts, False -> for question post
        # Step 1: set page, parameters
        page = 1
        api = self.get_api_url(str(page), is_answers)

        # Step 2: Send requests & Check if needed switch page
        # Parse 1st page
        data = requests.get(api).json()
        data_requests = [data]      # Collects all responses
        # print(data)
        # if it has more pages, construct a new requests for next page
        try:
            while data["has_more"]:
                # print("-"*20)
                page += 1
                api = self.get_api_url(str(page), is_answers)
                data = requests.get(api).json()
                data_requests.append(data)
                # print(page)
                # print(data)
                # print("-" * 20)
        except KeyError:
            print("No extra page")
        return data_requests

    # method: Get full question posts
    def get_questions(self):
        # Step 1: Collect Responses from API
        q_requests = self.get_stackexchange_response(False)

        # Step 2: Clean html tags & Construct StackData
        for r in q_requests:
            try:
                for q in r['items']:
                    # print(q)
                    self.__results.append({
                        "link": q["link"],
                        "tags": q["tags"],
                        "question": {
                            "id": q["question_id"],
                            "title": q["title"],
                            "content": self.get_pure_text(q["body"]),
                            "views" : q["view_count"]},
                        "answers": []
                    })
                    self.__questions.append(q["title"])
            except Exception as err:
                print(f"Unexpected {err=}, {type(err)=}")
                print("uh oh, q err")

    # method: Get all questions' full answers
    def get_answers(self):
        # Step 1: Collect all responses
        ans_requests = self.get_stackexchange_response(True)

        # Step 2:
        for r in ans_requests:
            try:
                for ans in r['items']:
                    idx = next((i for (i, d) in enumerate(self.__results)
                                if d["question"]["id"] == ans["question_id"]), None)
                    self.__results[idx]["answers"].append({
                        "id": ans["answer_id"],
                        "score": ans["score"],
                        "content": self.get_pure_text(ans["body"])
                    })
                    # print(ans)
            except Exception as err:
                print(f"Unexpected {err=}, {type(err)=}")
                print("uh oh, err :(")

    # get id list
    def get_ids(self):
        return self.__ids

    # cleaning html tags
    @staticmethod
    def get_pure_text(html):
        # get sentences without html tag & code
        soup = BeautifulSoup(html, 'html.parser')
        abstract = [i.text for i in soup.findAll('p')]
        result = " ".join(abstract)
        return result

    # display result
    def get_results(self):
        print(self.__results)
        return self.__results

    # Save to json file
    def save_results(self, file=""):
        timestamp = datetime.today().isoformat(sep="T", timespec="seconds").replace(":","-")
        with open(file+"StackData" + str(timestamp) + ".json", "w", encoding="utf-8") as f:
            json.dump(self.results, f)


def tester():
    test_urls = ['https://stackoverflow.com/questions/28461001/python-flask-cors-issue',
                 'https://stackoverflow.com/questions/75017173/cors-with-flask-axios-and-https-not-working-response-header-sends-origin-as-ht',
                 'https://stackoverflow.com/questions/21956683/enable-access-control-on-simple-http-server',
                 'https://stackoverflow.com/questions/70730067/csrf-token-cookie-is-not-set-for-cross-origin-requests',
                 'https://stackoverflow.com/questions/53298478/has-been-blocked-by-cors-policy-response-to-preflight-request-doesn-t-pass-acce',
                 'https://stackoverflow.com/questions/69056323/python-flask-limit-connection-to-requests-from-local-network-only',
                 'https://stackoverflow.com/questions/68813102/importerror-no-module-named-flask-cors',
                 'https://stackoverflow.com/questions/57236722/what-does-import-error-symbol-not-found-pqencryptpasswordconn-mean-and-how-do',
                 'https://stackoverflow.com/questions/25550337/http-post-request-header-field-access-control-allow-origin-is-not-allowed-by-ac',
                 'https://stackoverflow.com/questions/tagged/flask?tab=active&page=2']
    parser = StackData(test_urls)
    results = parser.get_results()
    return results


if __name__ == "__main__":
    print("Stack Overflow Parser v.0")
    t = tester()