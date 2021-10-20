import uvicorn

import json

with open("users.json", "r") as read_file:
	user_data = json.load(read_file)

# for i in user_data:
#     print(i['username'])

if __name__ == "__main__":
    uvicorn.run("app.api:app", host="0.0.0.0", port=8081, reload=True)
