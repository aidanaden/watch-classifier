from fastai.vision import *
from fastai.widgets import *
from starlette.applications import Starlette
from starlette.responses import JSONResponse, HTMLResponse, RedirectResponse
from io import BytesIO
from pprint import pprint
import uvicorn
import aiohttp
import asyncio
import requests

async def get_bytes(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.read()

app = Starlette()

defaults.device = torch.device('cpu')
learner_pth = Path('C:\\Users\\Aidan\\Documents\\DL Practice\\data\\watch_brands\\models')
learner_name = '1024-resnet34-90-watch-classification.pkl'
learner = load_learner(learner_pth, learner_name)

@app.route('/upload', methods=['POST'])
async def upload(request):
    data = await request.form()
    bytes = await (data['file'].read())
    return predict_img_from_bytes(bytes)

@app.route("/classify-url", methods=["GET"])
async def classify_url(request):
    bytes = await get_bytes(request.query_params["url"])
    return predict_img_from_bytes(bytes)

def predict_img_from_bytes(bytes):
    img = open_image(BytesIO(bytes))
    pred_clas, pred_idx, pred_probs = learner.predict(img)
    return JSONResponse({'prediction class': f'{pred_clas}', 
                         'prediction idx': f'{pred_idx}', 
                         'prediction_probs': f'{pred_probs}'})

@app.route('/')
def form(request):
    return HTMLResponse(
        """
        <form action='/upload' method='post' enctype='multipart/form-data'>
            Select image to upload:
            <input type='file' name='file'>
            <input type='submit' value='Upload Image'>
        </form>
        """
    )

@app.route('/form')
def redirect_to_homepage(request):
    return RedirectResponse('/')

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8008)