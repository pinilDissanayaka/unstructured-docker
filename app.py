import uvicorn
from routers.api import app

if __name__=="__main__":
    uvicorn.run(app=app,
                host="0.0.0.0", 
                port=5000)