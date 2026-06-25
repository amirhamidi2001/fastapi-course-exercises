from fastapi import FastAPI, HTTPException, status
from typing import List

app = FastAPI()

expense = [
    {"id": 1, "description": "Foo", "amount": 1.1},
    {"id": 2, "description": "Bar", "amount": 2.2},
    {"id": 3, "description": "Baz", "amount": 3.3},
]


# --- 1. GET ALL ITEMS (Status 200 OK) ---
@app.get("/items/", status_code=status.HTTP_200_OK)
async def read_items():
    return expense


# --- 2. GET ONE ITEM (Status 200 OK / 404 Not Found) ---
@app.get("/items/{id}", status_code=status.HTTP_200_OK)
def read_item(id: int):
    for item in expense:
        if item["id"] == id:
            return item

    # If the loop finishes without returning, the item was not found
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Expense with ID {id} not found."
    )


# --- 3. POST ITEM (Status 201 Created / 400 Bad Request) ---
@app.post("/items/{id}", status_code=status.HTTP_201_CREATED)
def post_item(id: int, description: str, amount: float):
    # Check if the ID already exists first
    for item in expense:
        if item["id"] == id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Expense with ID {id} already exists.",
            )

    new_item = {"id": id, "description": description, "amount": amount}
    expense.append(new_item)
    return {"message": "Expense added successfully", "data": new_item}


# --- 4. PUT ITEM (Status 200 OK / 404 Not Found) ---
@app.put("/items/{id}", status_code=status.HTTP_200_OK)
def update_item(id: int, description: str, amount: float):
    for item in expense:
        if item["id"] == id:
            item.update({"description": description, "amount": amount})
            return {"message": "Updated successfully", "data": item}

    # If loop finishes, item to update wasn't found
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Expense with ID {id} cannot be updated because it does not exist.",
    )


# --- 5. DELETE ITEM (Status 200 OK or 204 No Content / 404 Not Found) ---
@app.delete("/items/{id}", status_code=status.HTTP_200_OK)
def delete_item(id: int):
    for item in expense:
        if item["id"] == id:
            expense.remove(item)
            return {"message": "Item deleted successfully"}

    # If loop finishes, item to delete wasn't found
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Expense with ID {id} cannot be deleted because it does not exist.",
    )
