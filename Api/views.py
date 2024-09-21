from django.shortcuts import render
from cloudinary.uploader import upload_image, destroy
from django.http import JsonResponse

# Create your views here.

def image_upload(request):
    if request.method == 'POST':
        image = request.FILES['image']
        _i = upload_image(image)
        return JsonResponse(data={'url': _i.build_url()}, status=200, safe=False)
    else: 
        id = request.GET.get('id')
        if id:
            destroy(id)
            return JsonResponse(data={'message': 'Image deleted successfully'}, status=200)
        else:
            return JsonResponse(data={'error': 'Method not allowed'}, status=200)

