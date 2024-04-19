from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from models import RectangleRequest
import numpy as np
import base64
import cv2

import draw_rectangle_service
from crop_service import crop_image

app = FastAPI()

# CORS設定の追加
origins = [
    "http://localhost:3000",  # Next.jsアプリケーションのURL
    # 必要に応じて他のオリジンを追加
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/process-image/")
async def process_image(request: RectangleRequest):
    """
    複数の四角形の線を引いた画像を返却するエンドポイント。
    """
    data = request.dict()
    
    image_data = base64.b64decode(data['image_base64'])
    image = cv2.imdecode(np.frombuffer(image_data, np.uint8), cv2.IMREAD_COLOR)
    
    rectangles = data['rectangle_coords']
    color = tuple(data['color'])
    thickness = data['thickness']
    
    processed_image = draw_rectangle_service.process_image(image, rectangles, color, thickness)
    
    _, buffer = cv2.imencode('.png', processed_image)
    processed_image_base64 = base64.b64encode(buffer).decode('utf-8')
    
    return JSONResponse(content={'processed_image_base64': processed_image_base64})

@app.post("/crop-image/")
async def crop_image_api(request: RectangleRequest):
    """
    指定された四角形の座標に基づいて画像をクロップするエンドポイント。
    """
    data = request.dict()
    
    image_data = base64.b64decode(data['image_base64'])
    image = cv2.imdecode(np.frombuffer(image_data, np.uint8), cv2.IMREAD_COLOR)
    
    rectangles = data['rectangle_coords']

    cropped_images_base64 = []

    image_height, image_width = image.shape[:2]

    for rectangle_coords in rectangles:
        x, y, w, h = rectangle_coords
        
        # クロップ範囲の検証
        if x < 0 or y < 0 or x + w > image_width or y + h > image_height:
            raise HTTPException(status_code=400, detail="クロップ範囲が画像サイズを超えています。")
        
        cropped_image = crop_image(image, rectangle_coords)
        
        _, buffer = cv2.imencode('.png', cropped_image)
        cropped_image_base64 = base64.b64encode(buffer).decode('utf-8')
        
        cropped_images_base64.append(cropped_image_base64)
    
    return JSONResponse(content={'cropped_images_base64': cropped_images_base64})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
