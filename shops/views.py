# from django.shortcuts import render
from .models import Faces, Faces_in_shops, Locals, Shops, Staff, Staff_sell
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
import uuid
from django.contrib.auth import authenticate, login, logout

# MAILER
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.tokens import PasswordResetTokenGenerator

# read env
import environ

env = environ.Env(
    DEBUG=(bool, False)
)
environ.Env.read_env('.env')
# print(env('SITE_URL'))

# # START SERVER
# faces = Faces.objects.all()
# disc = np.zeros((1, 128), dtype=np.float64)
# # landArray = np.zeros((1, 128), dtype=np.float64)
# landArray = []
# idArray = np.zeros(len(faces), dtype=np.int)
# temp = b''
# for k, i in enumerate(faces):
#     if k == 0:
#         disc[0] = np.fromstring(temp.fromhex(i.landmarks), np.float64).reshape((1, 128))
#         idArray[0] = i.id
#
#     else:
#         landArray = np.fromstring(temp.fromhex(i.landmarks), np.float64)
#         landArray = landArray.reshape((1, 128))
#         disc = np.concatenate((disc, landArray), axis=0)
#         idArray[k] = i.id
# tree = spatial.KDTree(disc)
#
# print('////////////////////////////////////////////')
# print(len(disc))
# print('////////////////////////////////////////////')
#
# print('--------------------------------------------')
# print('                SERVER START                ')
# print('--------------------------------------------')
#
# from rest_framework.permissions import AllowAny, IsAuthenticated
# from .serializers import ShopSerializer, LocalsSerializer
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import authentication, permissions
# from rest_framework import status
#
# from rest_framework.decorators import api_view
# from rest_framework.decorators import permission_classes
#
#
# from rest_framework.schemas import SchemaGenerator
# from rest_framework_swagger import renderers
#
# import coreapi
# import coreschema
# from rest_framework.schemas import ManualSchema
#
#
# class SwaggerSchemaView(APIView):
#     permission_classes = [AllowAny]
#     renderer_classes = [
#         renderers.OpenAPIRenderer,
#         renderers.SwaggerUIRenderer
#     ]
#
#     def get(self, request):
#         generator = SchemaGenerator()
#         schema = generator.get_schema(request=request)
#         return Response(schema)
#
#
# from rest_framework_swagger.renderers import OpenAPIRenderer, SwaggerUIRenderer
# from rest_framework.decorators import api_view, renderer_classes
# from rest_framework import response, schemas
#
#
# @api_view()
# @renderer_classes([SwaggerUIRenderer, OpenAPIRenderer])
# def schema_view(request):
#     generator = schemas.SchemaGenerator(title='Pastebin API')
#     return response.Response(generator.get_schema(request=request))
#
#
# # API CREATE
# class CreateShopAPIView(APIView):
#     permission_classes = (AllowAny,)
#
#     def post(self, request):
#         user = request.data
#         serializer = ShopSerializer(data=user)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#
#         active_token = PasswordResetTokenGenerator().make_token(Shops.objects.get(email=request.data['email']))
#
#         subject, from_email, to = 'confirm your email', 'faceappmailer@gmail.com', request.data['email']
#         text_content = 'Confirmation of registration'
#         html_content = '<a href="' + env('SITE_URL') + '/face_tracking/confirm?token=' + str(active_token) + '&email=' + \
#                        request.data['email'] + '">Confirm Registretion</a>'
#         msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
#         msg.attach_alternative(html_content, "text/html")
#         msg.send()
#
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#
# from rest_framework_jwt.serializers import jwt_payload_handler
# import jwt
# from face_traking_api import settings
# from django.contrib.auth.hashers import Argon2PasswordHasher
#
# ph = Argon2PasswordHasher()
#
#
# @api_view(['POST'])
# @permission_classes([AllowAny, ])
# def authenticate_user(request):
#     try:
#         email = request.data['email']
#         password = request.data['password']
#
#         # shop = Shops.objects.get(email=email, password=password)
#         shop = Shops.objects.get(email=email)
#
#         if not (ph.verify(password, shop.password)):
#             res = {
#                 'error': 'invalid email of password'}
#             return Response(res, status.HTTP_422_UNPROCESSABLE_ENTITY)
#
#         if shop:
#             try:
#                 payload = jwt_payload_handler(shop)
#                 token = jwt.encode(payload, settings.SECRET_KEY)
#                 shop_details = {}
#                 shop_details['name'] = "%s" % (
#                     shop.email)
#                 shop_details['shop_uuid'] = shop.shop_uuid
#                 shop_details['token'] = token
#                 # user_logged_in.send(sender=shop.__class__,
#                 #                     request=request, shop=shop)
#                 return Response(shop_details, status=status.HTTP_200_OK)
#
#             except Exception as e:
#                 raise e
#         else:
#             res = {
#                 'error': 'can not authenticate with the given credentials or the account has been deactivated'}
#             return Response(res, status=status.HTTP_403_FORBIDDEN)
#     except KeyError:
#         res = {'error': 'please provide a email and a password'}
#         return Response(res)
#
#
# @api_view(['POST'])
# @permission_classes([IsAuthenticated, ])
# def get_locals_list(request):
#     locals_list = Locals.objects.filter(shop_uuid=request.user.shop_uuid)
#
#     if not (locals_list.exists()):
#         return Response({'error': 'There are no locals!'}, status=status.HTTP_404_NOT_FOUND)
#
#     serializer = LocalsSerializer(locals_list, many=True)
#     return Response(serializer.data, status=status.HTTP_200_OK)
#
#
# @api_view(['POST'])
# @permission_classes([IsAuthenticated, ])
# def authenticate_face(request):
#     try:
#
#         shop_uuid = request.data['shop_uuid']
#         local_id = request.data['local_id']
#         faces_pl = request.data['faces_landmark']
#
#         face_landmarks = np.fromstring(temp.fromhex(faces_pl), np.float64)
#         face_landmarks = face_landmarks.reshape((1, 128))
#
#         global disc, tree, idArray
#
#         a = tree.query([face_landmarks])
#
#         print(disc.shape)
#
#         if a[0][0] > 0.5:
#
#             disc = np.concatenate((disc, face_landmarks), axis=0)
#             tree = spatial.KDTree(disc)
#             f = Faces()
#             f.landmarks = request.data['faces_landmark']
#             f.save()
#
#             idArray = np.append(idArray, f.id)
#             print('------this is id array----------------')
#             print(idArray)
#             # TODO Shop_uuid
#             f.faces_in_shops_set.create(local_id=local_id, shop_id=shop_uuid)  # shop_id -> uuid
#             # print('------------FACE CREATED--------------')
#             return JsonResponse({'errors': '0',
#                                  'face_id': f.id,
#                                  'counts': '1',
#                                  'local_id': local_id})
#
#         else:
#             print('------this is a[1][0]----------------')
#             print(a[1][0])
#             m = a[1][0]
#             print('------this idArray[m]----------------')
#             print(idArray[m])
#             try:
#                 fis = Faces_in_shops.objects.get(face_id=idArray[a[1][0]], local_id=local_id)
#             # TODO Shop_uuid
#             except Faces_in_shops.DoesNotExist:
#                 Faces_in_shops.objects.create(face_id=idArray[a[1][0]], local_id=local_id, shop_id=shop_uuid)
#                 return Response({'errors': '0',
#                                  'face_id': idArray[a[1][0]],
#                                  'counts': '1',
#                                  'local_id': local_id}, status=status.HTTP_200_OK)
#             else:
#                 fis.counts = fis.counts + 1
#                 fis.save()
#                 return Response({'errors': '0',
#                                  'face_id': fis.face_id,
#                                  'counts': fis.counts,
#                                  'local_id': fis.local_id}, status=status.HTTP_200_OK)
#     except KeyError:
#         res = {'error': 'please provide a email and a password'}
#         return Response(res, status=status.HTTP_403_FORBIDDEN)
#
#     else:
#         return Response({'errors': '1000000'})
#
#
# from rest_framework.generics import RetrieveUpdateAPIView
#
#
# class ShopRetrieveUpdateAPIView(RetrieveUpdateAPIView):
#     # Allow only authenticated users to access this url
#     permission_classes = (IsAuthenticated,)
#     serializer_class = ShopSerializer
#
#     def get(self, request, *args, **kwargs):
#         # serializer to handle turning our `User` object into something that
#         # can be JSONified and sent to the client.
#         serializer = self.serializer_class(request.user)
#
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#     def put(self, request, *args, **kwargs):
#         serializer_data = request.data.get('user', {})
#
#         serializer = ShopSerializer(
#             request.user, data=serializer_data, partial=True
#         )
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#
#         return Response(serializer.data, status=status.HTTP_200_OK)


# ---------------------------------------------------------------------------------------------------

@csrf_exempt
def confirm(request):
    if request.method == 'GET':
        try:
            user = Shops.objects.get(email=request.GET['email'])
        except Shops.DoesNotExist:
            return render(request, 'registration/login.html', {'errors': 'Shop does not exist!'})
            # return HttpResponse(' Shop does not exist !')
        else:
            if (PasswordResetTokenGenerator().check_token(user, request.GET['token'])):
                user.is_active = True
                user.save()
                return render(request, 'registration/login.html', {'success': 'Sucsess activated!'})
                # return HttpResponse(' Activated sucsess! ')
            else:
                return render(request, 'registration/login.html', {'errors': 'Fail activate Shop!'})
                # return HttpResponse(' Fail activate Shop! ')

@csrf_exempt
def registration(request):
    if request.method == 'GET':
        return render(request, 'registration/login.html')


@csrf_exempt
def create(request):
    if request.method == 'POST':
        if not (request.POST['password'] == request.POST['confirm-password']):
            return render(request, 'registration/login.html', {'errors': "Passwords do not match"})
        try:
            s = Shops.objects.get(email=request.POST['email'])
        except Shops.DoesNotExist:
            s = Shops.objects.create_shop(email=request.POST['email'], password=request.POST['password'])
            s.name = request.POST['shop_name']
            # s.shop_uuid = uuid.uuid4()
            s.save()
            active_token = PasswordResetTokenGenerator().make_token(s)

            subject, from_email, to = 'confirm your email', 'faceappmailer@gmail.com', request.POST['email']
            text_content = 'Confirmation of registration'
            html_content = '<a href="' + env('SITE_URL') + '/face_tracking/confirm?token=' + str(active_token) + '&email=' + \
                           request.POST['email'] + '">Confirm Registretion</a>'
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            # request.session['shop_uuid'] = str(s.shop_uuid)
            # return HttpResponseRedirect(reverse('shops:shop_index'))
            return render(request, 'registration/login.html', {'success': 'Shop success create',
                                                               'info': 'Please confirm your email'})
        else:
            return render(request, 'registration/login.html', {'errors': "Shop already exist"})





@csrf_exempt
def log_in(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST['email'], password=request.POST['password'])
        if user:
            login(request, user)
            request.session['shop_uuid'] = str(user.shop_uuid)
            return HttpResponseRedirect(reverse('shops:shop_index'))
        else:
            return render(request, 'registration/login.html', {'errors': "Invalid email or password",
                                                               'info': 'Check email to activate shop'})


@csrf_exempt
def log_out(request):
    if request.method == "GET":
        logout(request)

        return HttpResponseRedirect(reverse('shops:shop_registration'))


@csrf_exempt
def add_local(request):
    if request.method == 'POST':
        try:
            local_name = request.POST['local_name']
            print(local_name)
            l = Locals()
            l.shop_id = request.session['shop_uuid']
            l.name = local_name
            l.save()

            return HttpResponseRedirect(reverse('shops:shop_index'))

        except KeyError:
            return render(request, 'shops/index.html', {'errors': 'KeyError'})

        else:
            return render(request, 'shops/index.html', {'errors': 'Something go wrong'})

@csrf_exempt
def index(request):
    if request.method == 'GET':
        try:
            locals_list = Locals.objects.filter(shop_id=request.session['shop_uuid'])
        except Locals.DoesNotExist:
            return render(request, 'shops/index.html', {})
        except KeyError:
            return render(reverse('shops:shop_login'))
        else:
            return render(request, 'shops/index.html', {'locals_list': locals_list, 'request': request})


def local_detail(request, local_id):
    if request.method == 'GET':
        if request.user.is_authenticated:
            faces_in_shop = Faces_in_shops.objects.filter(local_id=local_id)
            if not (faces_in_shop.exists()):
                return render(request, 'shops/local_details.html', {'errors': 'There are no faces'})
            else:
                return render(request, 'shops/local_details.html', {'faces_in_shop': faces_in_shop})
        else:
            return render(request, 'registration/login.html', {'errors': 'Please Sign in or Sign up'})

@csrf_exempt
def staff_create(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            Staff.objects.create(shop_id = request.session['shop_uuid'], name=request.POST['staff_name'])
            return HttpResponseRedirect (reverse('shops:staff_in_shops'))
        else:
            return render(request, 'registration/login.html', {'errors': 'Please Sign in or Sign up'})


def staff_index(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            staff_in_shop = Staff.objects.filter(shop_id = request.session['shop_uuid'])
            if not(staff_in_shop.exists()):
                return render(request, 'shops/staff_in_shops.html', {'errors': 'There are no stuff'})
            else:
                return render(request, 'shops/staff_in_shops.html', {'staff_in_shop': staff_in_shop})
        else:
            return render(request, 'registration/login.html', {'errors': 'Please Sign in or Sign up'})


def staff_detail(request, staff_id):
    if request.method == 'GET':
        if request.user.is_authenticated:
            staff_sell = Staff_sell.objects.filter(staff_id = staff_id)
            if not(staff_sell.exists()):
                return render(request, 'shops/staff_detail.html', {'errors': 'There are no sells'})
            else:
                return render(request, 'shops/staff_detail.html', {'staff_sell': staff_sell})
        else:
            return render(request, 'registration/login.html', {'errors': 'Please Sign in or Sign up'})


def test(request):
    if request.method == 'GET':
        return render(request, 'shops/graphic.html')