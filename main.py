import uvicorn

<<<<<<< HEAD
if __name__ == "__main__":
    uvicorn.run("app.api:app", host="0.0.0.0", port=8081, reload=True)
=======
with open("menu.json", "r") as read_file:
	menu_data = json.load(read_file)
app = FastAPI()

@app.get("/")
def root():
	return{"Menu":"Item"}

@app.get("/menu")
async def read_all_menu():
	return menu_data

@app.get("/menu/{item_id}")
async def read_menu(item_id: int):
	for menu_item in menu_data["menu"]:
		if menu_item["id"] == item_id:
			return menu_item
	raise HTTPException(
		status_code=404, detail=f"Item not found"
		)

@app.post("/menu")
async def write_menu(name:str):
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

@app.put("/menu/{item_id}")
async def update_menu(item_id: int, name:str):
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

@app.delete("/menu/{item_id}")
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
>>>>>>> master
