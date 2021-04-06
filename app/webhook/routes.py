from flask import Blueprint, json, request
from ..extensions import mydb

webhook = Blueprint('Webhook', __name__, url_prefix='/webhook')

@webhook.route('/receiver', methods=["POST"])
def receiver():
    mydict={"request_id":"","author":"","action":"","from_branch":"","to_branch":"","timestamp":""} #Schema for insertion into DataBase

    if request.headers.get('Content-Type')=='application/json':
        mycol=mydb["items"] #Replace items with your Collections name

        if request.json.get('action')=='opened': #Code that handels Pull Request
            pr_info=request.json["pull_request"]
            mydict["request_id"]=pr_info["id"]
            mydict["author"]=request.json.get('sender')['login']
            mydict["action"]="PR"
            mydict["from_branch"]=pr_info["head"]["label"]
            mydict["to_branch"]=pr_info["base"]["label"]
            mydict["timestamp"]=pr_info["created_at"]
            x=mycol.insert_one(mydict)

        elif request.json.get('action')=='closed': #Code that handels Merge
            pr_info=request.json["pull_request"]

            if pr_info['merged']==True:
                mydict["request_id"]=pr_info["id"]
                mydict["author"]=request.json.get('sender')['login']
                mydict["action"]="MR"
                mydict["from_branch"]=pr_info["head"]["label"]
                mydict["to_branch"]=pr_info["base"]["label"]
                mydict["timestamp"]=pr_info["created_at"]
                x=mycol.insert_one(mydict)

        if request.json.get('commits'): #Code that handels Push 
            for i in request.json.get('commits'):
                mydict["request_id"]=i["id"]
                mydict["author"]=i.get('author')['username']
                mydict["action"]="PUSH"
                mydict["from_branch"]=""
                mydict["to_branch"]=request.json.get('ref').split('/')[-1]
                mydict["timestamp"]=request.json.get('repository')['updated_at']
                try: 
                    x=mycol.insert_one(mydict)
                except:
                    pass

    return "SUCCESS"
