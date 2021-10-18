import json
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from jose import JWTError, jwt
from passlib.context import CryptContext

with open("data.json", "r") as read_file:
	data = json.load(read_file)

class UserInDB(User):
    hashed_password: str

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
app = FastAPI()

def verify_password(plain_password, hashed_password):
	return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
	return pwd_context.hash(password)

def get_user(db, username: str):
	if username in db:
		user_dict = db["user"]
		return UserInDB(**user_dict)

def authenticate_user(db, username: str, password: str):
	user = get_user(db, username)
	if not user:
		return False
	if not verify_password(password, user.hashed_password):
		return False
	return user

@app.get("/")
def root():
	return{"Menu":"Item"}

@app.get("/menu")
async def read_all_menu():
	return data

@app.get("/menu/{item_id}")
async def read_menu(item_id: int):
	for menu_item in data["menu"]:
		if menu_item["id"] == item_id:
			return menu_item
	raise HTTPException(
		status_code=404, detail=f"Item not found"
		)

@app.post("/menu")
async def write_menu(name:str):
	id=1
	if (len(data["menu"])>0):
		id = data["menu"][len(data["menu"])-1]["id"]+1
	new_data = {"id":id, "name":name}
	data['menu'].append(dict(new_data))
	read_file.close()
	with open("menu.json", "w") as write_file:
		json.dump(data,write_file,indent=4)
	write_file.close()

	return (new_data)
	raise HTTPException(
		status_code=500, detail=f"Internal Server Error"
		)

@app.put("/menu/{item_id}")
async def update_menu(item_id: int, name:str):
	for menu_item in data["menu"]:
		if menu_item["id"] == item_id:
			menu_item["name"] = name
			read_file.close()
			with open("menu.json", "w") as write_file:
				json.dump(data,write_file,indent=4)
			write_file.close()

			return{"message":"Data updated successfully"}

	raise HTTPException(
		status_code=404, detail=f"Item not found"
		)

@app.delete("/menu/{item_id}")
async def delete_menu(item_id: int):
	for menu_item in data["menu"]:
		if menu_item["id"] == item_id:
			data["menu"].remove(menu_item)
			read_file.close()
			with open("menu.json", "w") as write_file:
				json.dump(data,write_file,indent=4)
			write_file.close()

			return{"message":"Data deleted successfully"}

	raise HTTPException(
		status_code=404, detail=f"Item not found"
		)


# ,
#     "user": [
#         {
#             "id": 1,
#             "username": "jondhoe",
#             "full_name": "John Doe",
#             "email": "johndoe@example.com",
#             "hashed password": "16fe6a11d103b986bc8da2992e8772a1ea1fe88670594636c0421cbddbc55f4c",
#             "disabled": False,
#         },
#         {
#             "id": 2,
#             "username": "jondhoe2",
#             "full_name": "John Doe 2",
#             "email": "johndoe2@example.com",
#             "hashed password": "b298699bc7933d904e479afc826043f6e78da864c8672c92e292f91021a4eade",
#             "disabled": False,
#         }
#     ]