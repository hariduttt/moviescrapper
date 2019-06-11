import json

response = json.dumps(json.loads(open("movie_data.json","r").read()))
print(type(response))