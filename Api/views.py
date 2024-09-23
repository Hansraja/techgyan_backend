from django.shortcuts import render
from cloudinary.uploader import upload_image, destroy
from django.http import JsonResponse

def image_upload(request):
    if request.method == 'POST':
        image = request.FILES.get('image', None)
        if not image:
            return JsonResponse(data={'error': 'No image provided'}, status=400)
        try:
            image = upload_image(image)
            return JsonResponse(data={'url': image.build_url(), 'id': image.public_id, 'format': image.format}, status=200, safe=False)
        except: 
            return JsonResponse(data={'error': 'Image upload failed'}, status=400)
    else: 
        id = request.GET.get('id')
        if id:
            dt = destroy(id)
            return JsonResponse(data={'message': f'Image deleted successfully {str(dt)}'}, status=200)
        else:
            return JsonResponse(data={'error': 'Method not allowed'}, status=200)

