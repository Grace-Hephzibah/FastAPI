from fastapi import FastAPI, Path, Query
from fastapi import HTTPException, status # Helps to use status codes

# Recommended by FastAPI
from typing import Optional

# Used for posting data (Check out the Post Section)
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float
    brand: Optional[str] = None

# Update Item is the same as Item
# But all the parameters are optional
# Users can send the data that must be updated and
# ignore the others with the same value
class UpdateItem(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    brand: Optional[str] = None

# Run the file as
# uvicorn <name of file without extension>:<name of the FastAPI object> -- reload
# Ex: uvicorn main:app --reload

# Local host : http://127.0.0.1:8000
# Documentation : http://127.0.0.1:8000/docs

app = FastAPI()

# Possible Operations
## GET POST PUT DELETE

# Get -> Access the api and requests some value
# Post -> You send value to the API
# Put -> Update the values or modifying
# Delete -> Deletes the value

# Inventory data -> has to be a object of the class Item
# So,
# inventory = {
#    1 : {
#        "name" : "milk",
#        "price" : 3.99,
#        "brand" : "Regular"
#    }
#}

inventory = {}

################################################
############## GET #############################
################################################

@app.get("/") # Setting up a end point
def home():
    return {"Welcome" : "To Our Store"}

# Path Parameters
@app.get("/get-item/{item_id}")
def get_item(item_id : int): # item_id : int -> type casting
    return inventory[item_id]

#@app.get("/get-detail/{item_id}/{name}")
#def get_detail(item_id : int, name : str):
#    return {"Value" : inventory[item_id][name]}

# Using Path in the FastAPI
@app.get("/item-path/{item_id}")
def item_path(item_id: int = Path(None, # This is the default value
                    description = "The ID of the item you would like to view",
                    gt = 0)):
    return inventory[item_id]

# gt -> greater than
# lt -> lesser than
# le -> less than or equal to
# ge -> greater than or equal to

# Query parameter
@app.get("/get-by-name")
def get_by_name(name: Optional[str] = None): # Write the non default arguments first and then the default arguments
                                             # Or  def get_by_name(*, name: Optional[str] = None, test: int):
                                             # Both works
    for item_id in inventory:
        #if inventory[item_id]["name"] == name:
        if inventory[item_id].name == name:
            return inventory[item_id]

    # return {"Data" : "Not Found "}
# Using status codes
    raise HTTPException(status_code = 404, detail = "Data Not Found") # Instead of 404 you can type status.HTTP_404_NOT_FOUND
    # There are codes and you need to check them out

################################################
############## POST ############################
################################################

@app.post("/create-item/ {item_id}")
def create_item(item_id: int, item : Item):
    if item_id in inventory:
        # return {"Error" : "Item ID Already Exists"}
        # Using status codes
        raise HTTPException(status_code=404,
                            detail="Item ID Already Exist")

    #inventory[item_id] = {
    #                      "name" : item.name,
    #                      "brand" : item.brand,
    #                      "price" : item.price
    #                      }

    inventory[item_id] = item # can insert the object itself
    return inventory[item_id]

# But we need to change inventory[item_id]["name"] ---> inventory[item_id].name


################################################
############## PUT #############################
################################################

@app.put("/update-item/{item_id}")
def update_item(item_id : int, item : UpdateItem):
    if item_id not in inventory:
        # return {"Error" : "Item ID Does Not Exists"}
        # Using status codes
        raise HTTPException(status_code=404,
                            detail="Item ID Does Not Exist")

        # Updates item_id
    if item.name != None:
        inventory[item_id].name = item.name

    if item.price != None:
        inventory[item_id].price = item.price

    if item.brand != None:
        inventory[item_id].brand = item.brand

    return inventory[item_id]

################################################
############## DELETE ##########################
################################################

@app.delete("/delete-item")
def delete_item(item_id : int = Query(..., description = " ID of item to delete", gt = 0)):
    if item_id not in inventory:
        # return {"Error" : "ID does not exist"}
        # Using status codes
        raise HTTPException(status_code=404,
                            detail="Item ID Does Not Exist")

    del inventory[item_id]
    return {"Done" : "Item Deleted"}