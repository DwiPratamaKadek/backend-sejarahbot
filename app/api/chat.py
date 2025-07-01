from fastapi import APIRouter, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
from typing import Optional
import io
from PIL import Image
from app.services.rag_engine import build_qa
from transformers import BlipProcessor, BlipForConditionalGeneration
import torch

router = APIRouter()
qa_chain = build_qa()

processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

def get_image_caption(image_pil: Image.Image) -> str:
    inputs = processor(images=image_pil, return_tensors="pt")
    output = model.generate(**inputs)
    caption = processor.decode(output[0], skip_special_tokens=True)
    return caption

@router.post("/image-chat")
async def image_chat(
    query: str = Form(...),
    image: Optional[UploadFile] = None
):
    try:
        result = qa_chain(query)
        answer = result["result"]
        response_text = answer

        if image:
            contents = await image.read()
            img = Image.open(io.BytesIO(contents))
            caption = get_image_caption(img)
            response_text += f"\Deskripsi Gambar :  {caption}"

        return JSONResponse({"question": query, "answer": response_text})

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
