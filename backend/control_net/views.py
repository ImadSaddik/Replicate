import io
import json
import base64
import replicate
from dotenv import load_dotenv
from urllib.parse import urlparse

from django.http import JsonResponse
from rest_framework.decorators import api_view


@api_view(['POST'])
def getImages(request):
    load_dotenv()
    data = json.loads(request.body)
    
    prompt = data['prompt']
    num_samples = data['num_samples']
    image_resolution = data['image_resolution']
    buffered_reader, image_buffer = getImageBuffer(data['image'])
    
    output = replicate.run(
        "jagilley/controlnet-scribble:435061a1b5a4c1e26740464bf786efdfa9cb3a3ac488595a2de23e143fdb0117",
        input={
            "image": buffered_reader,
            "prompt":prompt,
            "num_samples":str(num_samples),
            "image_resolution":str(image_resolution),
        }
    )
    
    image_buffer.close()
    
    return JsonResponse(output[1:], safe=False)


def getImageBuffer(imageUri):
    parsed_uri = urlparse(imageUri)
    
    base64_data = parsed_uri.path.split(',')[1]
    image_bytes = base64.b64decode(base64_data)

    image_buffer = io.BytesIO(image_bytes)
    buffered_reader = io.BufferedReader(image_buffer)
    
    return buffered_reader, image_buffer

