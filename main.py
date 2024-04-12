from fastapi import FastAPI
import httpx
import json
import pandas
import uuid

app = FastAPI()
package = "pandas"
url = f"https://api.stackexchange.com/2.3/search?order=desc&sort=votes&tagged={package}&site=stackoverflow"
randomString = str(uuid.uuid4())

@app.get("/")
def root():
  response = httpx.get(url)
  jsonObject =  json.loads(response.text)
  csvList = []
  for item in jsonObject["items"]:
    qurl = f"https://api.stackexchange.com/2.3/questions/{item["question_id"]}/comments?order=desc&sort=creation&site=stackoverflow"
    qresponse = httpx.get(qurl)
    qjsonObject = json.loads(qresponse.text)
    csvList.append(item["title"])
    print(f"question: {item["title"]}")
    for qitem in qjsonObject["items"]:
      curl = f"https://api.stackexchange.com/2.3/comments/{qitem["comment_id"]}?order=desc&sort=creation&site=stackoverflow&filter=!nNPvSN_ZTx"
      cresponse = httpx.get(curl)
      cjsonObject = json.loads(cresponse.text)
      csvList.append(cjsonObject["items"][0]["body"])
      print(f"comment: {cjsonObject["items"][0]["body"]}")
    
  dict = {"text": csvList}
  df = pandas.DataFrame(dict)
  df.to_csv(f'{randomString}.csv', index=False, header=False)
    
  return csvList