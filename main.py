import json

from fastapi import FastAPI, HTTPException, Body, Depends

from app.auth.auth_bearer import JWTBearer
from app.auth.auth_handler import signJWT
from app.auth.auth_hashing import get_password_hash, check_user

from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

with open("menu.json", "r") as read_file:
	menu_data = json.load(read_file)

with open("users.json", "r") as read_file:
	user_data = json.load(read_file)
    
app = FastAPI()

# get

@app.get("/", dependencies=[Depends(JWTBearer())], tags=["root"])
async def root() -> dict:
	return{"Menu":"Item"}


@app.get("/menu", dependencies=[Depends(JWTBearer())], tags=["menu"])
async def read_all_menu() -> dict:
	return menu_data

@app.get("/menu/{item_id}", dependencies=[Depends(JWTBearer())], tags=["menu"])
async def read_menu(item_id: int) -> dict:
	for menu_item in menu_data["menu"]:
		if menu_item["id"] == item_id:
			return menu_item
	raise HTTPException(
		status_code=404, detail=f"Item not found"
		)

#post

@app.post("/menu", dependencies=[Depends(JWTBearer())], tags=["menu"])
async def add_menu(name: str) -> dict:
	id=1
	if (len(menu_data["menu"])>0):
		id = menu_data["menu"][len(menu_data["menu"])-1]["id"]+1
	new_data = {"id":id, "name":name}
	menu_data['menu'].append(dict(new_data))
	read_file.close()
	with open("menu.json", "w") as write_file:
		json.dump(menu_data,write_file,indent=4)
	write_file.close()

	return (new_data)
	raise HTTPException(
		status_code=500, detail=f"Internal Server Error"
		)

# put

@app.put("/menu/{item_id}", dependencies=[Depends(JWTBearer())], tags=["menu"])
async def update_menu(item_id: int, name: str):
	for menu_item in menu_data["menu"]:
		if menu_item["id"] == item_id:
			menu_item["name"] = name
			read_file.close()
			with open("menu.json", "w") as write_file:
				json.dump(menu_data,write_file,indent=4)
			write_file.close()

			return{"message":"Data updated successfully"}

	raise HTTPException(
		status_code=404, detail=f"Item not found"
		)

# delete

@app.delete("/menu/{item_id}", dependencies=[Depends(JWTBearer())], tags=["menu"])
async def delete_menu(item_id: int):
	for menu_item in menu_data["menu"]:
		if menu_item["id"] == item_id:
			menu_data["menu"].remove(menu_item)
			read_file.close()
			with open("menu.json", "w") as write_file:
				json.dump(menu_data,write_file,indent=4)
			write_file.close()

			return{"message":"Data deleted successfully"}

	raise HTTPException(
		status_code=404, detail=f"Item not found"
		)

# user
# signup

@app.post("/user/signup", tags=["user"])
async def create_user(username: str, password: str):
	for user in user_data:
		if user['username'] == username:
			raise HTTPException (status_code=301, detail=f"user already exist")
	hashed = get_password_hash(password)
	new_data = {"username":username, "password":hashed}
	user_data.append(dict(new_data))
	read_file.close()
	with open("users.json", "w") as write_file:
		json.dump(user_data,write_file,indent=4)
	write_file.close()
	return signJWT(username)

# login

@app.post("/user/login", tags=["user"])
async def user_login(username: str, password: str):
    if check_user(username, password):
        return signJWT(username)
    return {
        "error": "Wrong login details!"
    }

# read all user

@app.get("/user", dependencies=[Depends(JWTBearer())], tags=["user"])
async def read_all_user() -> dict:
	return user_data
