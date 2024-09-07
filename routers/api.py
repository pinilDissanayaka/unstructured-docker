from fastapi import FastAPI, HTTPException, status, UploadFile
from utils.resources import extract_text_from_docs



app=FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/extract-text", tags=['user'])
async def uploadResource(docs:list[UploadFile]):
    try:
        text_elements, table_elements, image_elements=extract_text_from_docs(docs=docs)
        return {
            "detail" : "done",
            "text_elements":text_elements,
            "table_elements":table_elements,
            "image_elements":image_elements
            }
        
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                            detail=e.args)