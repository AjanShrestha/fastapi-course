from fastapi import FastAPI
from fastapi.params import Body

app = FastAPI()


# Path Operation / Route
# Decorator converts the function into a path operation
# Makes it an API that can be called
# decorator - object.HTTPFunction(Params)
# Path operation converts function into API
@app.get("/")
def root():
    # Converts it to JSON
    return {"message": "Hello World!"}


@app.get("/posts")
def get_posts():
    return [
        {
            "id": 1,
            "title": "Post 1",
            "body": "This is post 1",
        },
        {
            "id": 2,
            "title": "Post 2",
            "body": "This is post 2",
        },
        {
            "id": 3,
            "title": "Post 3",
            "body": "This is post 3",
        },
    ]


@app.post("/createposts")
# extract all the params from the request body,
# convert it into python dictionarym, and
# store it inside variable paylopad
def create_posts(payload: dict = Body(...)):
    print(payload)
    return {"new_post": f"title: {payload['title']} content: {payload['content']}"}
