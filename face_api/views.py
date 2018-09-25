# from django.shortcuts import render
from shops.models import Faces, Faces_in_shops, Locals, Shops, Staff_sell
from django.http import JsonResponse

from rest_framework_jwt.serializers import jwt_payload_handler
import jwt
from face_traking_api import settings
from django.contrib.auth.hashers import Argon2PasswordHasher

from rest_framework_swagger.renderers import OpenAPIRenderer, SwaggerUIRenderer
from rest_framework.decorators import api_view, renderer_classes
from rest_framework import response, schemas

import numpy as np
# from django.utils import timezone
from scipy import spatial

# read env
import environ

env = environ.Env(
    DEBUG=(bool, False)
)
environ.Env.read_env('.env')
# print(env('SITE_URL'))

# START SERVER
faces = Faces.objects.all()
disc = np.zeros((1, 128), dtype=np.float64)
# landArray = np.zeros((1, 128), dtype=np.float64)
landArray = []
idArray = np.zeros(len(faces), dtype=np.int)
temp = b''
for k, i in enumerate(faces):
    if k == 0:
        disc[0] = np.fromstring(temp.fromhex(i.landmarks), np.float64).reshape((1, 128))
        idArray[0] = i.id

    else:
        landArray = np.fromstring(temp.fromhex(i.landmarks), np.float64)
        landArray = landArray.reshape((1, 128))
        disc = np.concatenate((disc, landArray), axis=0)
        idArray[k] = i.id
tree = spatial.KDTree(disc)

print('////////////////////////////////////////////')
print(len(disc))
print('////////////////////////////////////////////')

print('--------------------------------------------')
print('                SERVER START                ')
print('--------------------------------------------')

from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import ShopSerializer, LocalsSerializer, FacesInShopDetailSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.decorators import permission_classes

# MAILER
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from rest_framework.schemas import SchemaGenerator
from rest_framework_swagger import renderers

import coreapi
import coreschema
from rest_framework.schemas import ManualSchema


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
# @api_view()
# @renderer_classes([SwaggerUIRenderer, OpenAPIRenderer])
# def schema_view(request):
#     generator = schemas.SchemaGenerator(title='Pastebin API')
#     return response.Response(generator.get_schema(request=request))

from rest_framework.schemas import AutoSchema

#
# # API CREATE
# class CreateShopAPIView(APIView):
#     permission_classes = [AllowAny]
#     renderer_classes = [
#         renderers.OpenAPIRenderer,
#         renderers.SwaggerUIRenderer
#     ]
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
#         # generator = SchemaGenerator()
#         # schema = generator.get_schema(request=request)
#
#         return Response(serializer.data, status=status.HTTP_201_CREATED)


ph = Argon2PasswordHasher()


@api_view(['POST'])
@permission_classes([AllowAny, ])
def authenticate_user(request):
    try:
        email = request.data['email']
        password = request.data['password']

        shop = Shops.objects.get(email=email)

        if not (ph.verify(password, shop.password)):
            res = {
                'error': 'invalid email of password'}
            return Response(res, status.HTTP_422_UNPROCESSABLE_ENTITY)

        if shop:
            try:
                payload = jwt_payload_handler(shop)
                token = jwt.encode(payload, settings.SECRET_KEY)
                shop_details = {}
                shop_details['name'] = "%s" % (
                    shop.email)
                shop_details['shop_uuid'] = shop.shop_uuid
                shop_details['token'] = token
                # user_logged_in.send(sender=shop.__class__,
                #                     request=request, shop=shop)
                return Response(shop_details, status=status.HTTP_200_OK)

            except Exception as e:
                raise e
        else:
            res = {
                'error': 'can not authenticate with the given credentials or the account has been deactivated'}
            return Response(res, status=status.HTTP_403_FORBIDDEN)
    except KeyError:
        res = {'error': 'please provide a email and a password'}
        return Response(res)


@api_view(['POST'])
@permission_classes([IsAuthenticated, ])
def get_locals_list(request):
    print(request.user.shop_uuid)
    locals_list = Locals.objects.filter(shop_id=request.user.shop_uuid)
    print(locals_list)

    if not (locals_list.exists()):
        return Response({'error': 'There are no locals!'}, status=status.HTTP_404_NOT_FOUND)

    serializer = LocalsSerializer(locals_list, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny, ])
def authenticate_face(request):
    try:
        shop_uuid = request.data['shop_uuid']
        local_id = request.data['local_id']
        faces_pl = request.data['faces_landmark']

        face_landmarks = np.fromstring(temp.fromhex(faces_pl), np.float64)
        face_landmarks = face_landmarks.reshape((1, 128))

        global disc, tree, idArray

        a = tree.query([face_landmarks])

        print(disc.shape)

        if a[0][0] > 0.5:

            disc = np.concatenate((disc, face_landmarks), axis=0)
            tree = spatial.KDTree(disc)
            f = Faces()
            f.landmarks = request.data['faces_landmark']
            f.save()

            idArray = np.append(idArray, f.id)
            f.faces_in_shops_set.create(local_id=local_id, shop_id=shop_uuid)  # shop_id -> uuid
            return Response({'errors': '0',
                             'face_id': f.id,
                             'counts': '1',
                             'local_id': local_id}, status=status.HTTP_200_OK)

        else:
            try:
                fis = Faces_in_shops.objects.get(face_id=idArray[a[1][0]], local_id=local_id)
            except Faces_in_shops.DoesNotExist:
                Faces_in_shops.objects.create(face_id=idArray[a[1][0]], local_id=local_id, shop_id=shop_uuid)
                return Response({'errors': '0',
                                 'face_id': idArray[a[1][0]],
                                 'counts': '1',
                                 'local_id': local_id}, status=status.HTTP_200_OK)
            else:
                fis.counts = fis.counts + 1
                fis.save()
                return Response({'errors': '0',
                                 'face_id': fis.face_id,
                                 'counts': fis.counts,
                                 'local_id': fis.local_id}, status=status.HTTP_200_OK)
    except KeyError:
        res = {'error': 'please provide a email and a password'}
        return Response(res, status=status.HTTP_403_FORBIDDEN)

    else:
        return Response({'errors': '1000000'})


class ShopRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    # Allow only authenticated users to access this url
    permission_classes = (IsAuthenticated,)
    serializer_class = ShopSerializer

    def get(self, request, *args, **kwargs):
        # serializer to handle turning our `User` object into something that
        # can be JSONified and sent to the client.
        serializer = self.serializer_class(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        serializer_data = request.data.get('user', {})

        serializer = ShopSerializer(
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


# STAFF

@api_view(['POST'])
@permission_classes([AllowAny,])
def face_in_shop_detail(request):
    try:
        # local_id = request.data['local_id']
        face_id = request.data['face_id']

        fis = Faces_in_shops.objects.filter(face_id = face_id)
        print(fis.count())

        if not(fis.exists()):
            return Response({'error': '10'}, status = status.HTTP_404_NOT_FOUND)

        else:
            serializer = FacesInShopDetailSerializer(fis, many=True)
            return Response(serializer.data, status = status.HTTP_200_OK)
    except KeyError:
        # TODO add error!
        return Response({'error': '1'}, status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated,])
def add_cash(request):
    try:
        local_id = request.data['local_id']
        cash = request.data['cash']
        face_id = request.data['face_id']
        staff_id = request.data['staff_id']

        print(local_id, cash, face_id, staff_id)

        try:
            f = Faces_in_shops.objects.get(face_id=face_id, local_id=local_id)
            f.cash = f.cash + int(cash)
            f.save()

            Staff_sell.objects.create(cash=cash, local_id=local_id, staff_id=staff_id)

            return Response({'error': '0'},
                            status=status.HTTP_200_OK)

        except Faces_in_shops.DoesNotExist:
            return Response({'error': '0'}, status=status.HTTP_404_NOT_FOUND)

    except KeyError:
        # TODO add error!
        return Response({'error': '1'}, status.HTTP_400_BAD_REQUEST)
