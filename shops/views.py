# from django.shortcuts import render
from .models import Faces, Faces_in_shops, Locals, Shops
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import numpy as np
# from django.utils import timezone
from scipy import spatial
import uuid
#read env
import environ
env = environ.Env(
    DEBUG=(bool, False)
)
environ.Env.read_env('.env')
# START SERVER
faces = Faces.objects.all()
disc = np.zeros((1, 128), dtype=np.float64)
# landArray = np.zeros((1, 128), dtype=np.float64)
landArray = []
idArray = np.zeros(len(faces), dtype=np.int)
temp = b''
for k, i in enumerate(faces):
    if k == 0:
        disc[0] = np.fromstring(temp.fromhex(i.landmarks), np.float64).reshape((1,128))
        idArray[0] = i.id

    else:
        landArray = np.fromstring(temp.fromhex(i.landmarks), np.float64)
        landArray = landArray.reshape((1,128))
        disc = np.concatenate((disc, landArray), axis=0)
        idArray[k] = i.id
tree = spatial.KDTree(disc)

print('////////////////////////////////////////////')
print(len(disc))
print('////////////////////////////////////////////')


print('--------------------------------------------')
print('                SERVER START                ')
print('--------------------------------------------')


def authKey(authKey):
    #TODO
    return 1


@csrf_exempt
def create(request):
    if request.method == 'POST':
        s = Shops.objects.create_shop(email=request.POST['email'], password=request.POST['password'])
        s.name = request.POST['shop_name']
        s.shop_uuid = uuid.uuid4()
        s.save()
        return HttpResponse(s.name)


@csrf_exempt
def index(request):
    if request.method == 'GET':
        # if not(authKey(request.GET['auth_key'])):
        #     return JsonResponse({'error' : '10'})
        faces = Faces.objects.all()
        count = len(faces)
        # disc = np.zeros((len(faces),128), dtype=np.float64)
        # print ('THIS IS COUNT FACES', len(faces))
        # for k, i in enumerate(faces):
        #     disc[k] = i.landmarks
        # return JsonResponse({'landmarks': disc})
        return JsonResponse({'errors':'0',
                             'faces': count})

    if request.method == 'POST':
        if not(authKey(request.POST['auth_key'])):
            return JsonResponse({'error' : '10'})
        face_landmarks = np.fromstring(temp.fromhex(request.POST['faces_landmark']), np.float64)
        face_landmarks = face_landmarks.reshape((1, 128))
        # print(face_landmarks)

        global disc, tree, idArray

        a = tree.query([face_landmarks])
        # print(a[0][0])



        print(disc.shape)

        if a[0][0] > 0.5:

            disc = np.concatenate((disc, face_landmarks), axis=0)
            tree = spatial.KDTree(disc)
            f = Faces()
            f.landmarks = request.POST['faces_landmark']
            f.save()

            print(f)

            idArray = np.append(idArray, f.id)

            print(idArray)

            f.faces_in_shops_set.create(counts = 0, local_id=2, shop_id = '008f320d-40ce-4aea-a73e-d37175a000d0')
            # print('------------FACE CREATED--------------')
            return JsonResponse({'errors': '0',
                                 'face_id': f.id,
                                 'counts': 0,
                                 'local_id': 2})

        else:
            # print(a[1][0])
            # m = a[1][0]
            # print(idArray[m])

            fis = Faces_in_shops.objects.get(face_id = idArray[a[1][0]])
            fis.counts = fis.counts + 1
            fis.save()
            return JsonResponse({'errors': '0',
                                 'face_id': fis.face_id,
                                 'counts': fis.counts,
                                 'local_id': fis.local_id})


@csrf_exempt
def show(request, user_id):
    if request.method == 'GET':
        # if not(authKey(request.GET['auth_key'])):
        #     return JsonResponse({'error':'10'})
        try:
            f = Faces.objects.get(id = user_id)
        except(Faces.DoesNotExist):
            return JsonResponse({'error': '20'})
        else:
            return JsonResponse({'error': '0',
                                 'landmark': f.landmarks,
                                 'created_at': f.created_at})
    return JsonResponse({'error': '0'})

@csrf_exempt
def destroy(request):
    if request.method == 'DELETE':
        # if not(authKey(request.DELETE['auth_key'])):
        #     return JsonResponse({'error': '10'})
        try:
            face = Faces.objects.get(id = request.GET['id'])
        except(Faces.DoesNotExist):
            return JsonResponse({'error': '20'})
        else:
            face.delete()
    return JsonResponse({'error': '0'})




