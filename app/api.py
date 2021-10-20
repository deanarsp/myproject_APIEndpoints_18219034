import json

from fastapi import FastAPI, HTTPException, Body, Depends

from app.model import MenuSchema, UserSchema, UserLoginSchema
from app.auth.auth_bearer import JWTBearer
from app.auth.auth_handler import signJWT

from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

posts = [
    {
        "id": 1,
        "title": "Pancake",
        "content": "Lorem Ipsum ..."
    }
]

users = []

with open("menu.json", "r") as read_file:
	menu_data = json.load(read_file)
    
app = FastAPI()

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

@app.post("/menu", dependencies=[Depends(JWTBearer())], tags=["menu"])
async def add_menu(menu: MenuSchema) -> dict:
	id=1
	if (len(menu_data["menu"])>0):
		id = menu_data["menu"][len(menu_data["menu"])-1]["id"]+1
	new_data = {"id":id, "name":menu.name}
	menu_data['menu'].append(dict(new_data))
	read_file.close()
	with open("menu.json", "w") as write_file:
		json.dump(menu_data,write_file,indent=4)
	write_file.close()

	return (new_data)
	raise HTTPException(
		status_code=500, detail=f"Internal Server Error"
		)

@app.put("/menu/{item_id}", dependencies=[Depends(JWTBearer())], tags=["menu"])
async def update_menu(menu: MenuSchema):
	for menu_item in menu_data["menu"]:
		if menu_item["id"] == menu.item_id:
			menu_item["name"] = menu.name
			read_file.close()
			with open("menu.json", "w") as write_file:
				json.dump(menu_data,write_file,indent=4)
			write_file.close()

			return{"message":"Data updated successfully"}

	raise HTTPException(
		status_code=404, detail=f"Item not found"
		)

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

# @app.post("/posts", dependencies=[Depends(JWTBearer())], tags=["posts"])
# async def add_post(post: PostSchema) -> dict:
#     post.id = len(posts) + 1
#     posts.append(post.dict())
#     return {
#         "data": "post added."
#     }

@app.post("/user/signup", tags=["user"])
async def create_user(user: UserSchema = Body(...)):
    users.append(user) # replace with db call, making sure to hash the password first
    return signJWT(user.email)

def check_user(data: UserLoginSchema):
    for user in users:
        if user.email == data.email and user.password == data.password:
            return True
    return False

@app.post("/user/login", tags=["user"])
async def user_login(user: UserLoginSchema = Body(...)):
    if check_user(user):
        return signJWT(user.email)
    return {
        "error": "Wrong login details!"
    }
