from fastapi import FastAPI
import httpx
import json
import pandas
import uuid

# CHANGE THIS TO SOMETHING DIFFERENT
package = "Scipy"

app = FastAPI()


@app.get("/")
def root():
  index = 0
  csvList = []
  
  response = httpx.get(f"https://api.stackexchange.com/2.3/search?order=desc&sort=votes&tagged={package}&site=stackoverflow")
  jsonObject =  json.loads(response.text)
  for item in jsonObject["items"]:
    qresponse = httpx.get(f"https://api.stackexchange.com/2.3/questions/{item["question_id"]}/comments?order=desc&sort=creation&site=stackoverflow")
    qjsonObject = json.loads(qresponse.text)
    index += 1
    csvList.append(item["title"])
    print(f"Added field #{index}")
    for qitem in qjsonObject["items"]:
      cresponse = httpx.get(f"https://api.stackexchange.com/2.3/comments/{qitem["comment_id"]}?order=desc&sort=creation&site=stackoverflow&filter=!nNPvSN_ZTx")
      cjsonObject = json.loads(cresponse.text)
      index += 1
      csvList.append(cjsonObject["items"][0]["body"])
      print(f"Added field #{index}")
    
  print(f"Added {index} fields for tag {package}")
  dict = {"text": csvList}
  df = pandas.DataFrame(dict)
  df.to_csv(f'{package}_{str(uuid.uuid4())[:5]}.csv', index=False, header=False)
    
  return csvList