import json

from django.db import transaction
from instaloader import LoginException, BadResponseException
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password, check_password
from insta.models import Insta, InstaHistory, InstaFuncType
from insta.serializers import InstaUserCreateSerializer
from insta.utils import check_insta_login
from share.functions import return_login_insta_instance, post_shortcode_downloader
from utils.response import Response

import time


class InstaUserApi(APIView):
    def post(self, request):
        insta_id = request.data.get('id', None)
        insta_pw = make_password(request.data.get('pw', None))
        ip_address = request.META.get('REMOTE_ADDR', request.META.get('HTTP_X_FORWARDED_FOR', '0,0,0,0'))

        if insta_id is None or insta_pw is None:
            return Response(data={'error': 'Missing id or pw'}, status=400)

        try:
            return_login_insta_instance(insta_id, request.data.get('pw', None))
        except LoginException as e:
	        if 'Checkpoint required' in str(e):
		        pass
	        else:
		        return Response(
			        data=str(e),
			        status=490
			        )

        try:
            # Insta 모델에서 기존 사용자 찾기
            insta = Insta.objects.get(name=insta_id)
            # 비밀번호 검증 후 IP 저장
            if check_password(insta_pw, insta.password):
	            if insta.IP != ip_address:
		            insta.IP = ip_address
		            insta.save()

        except Insta.DoesNotExist:
            # 사용자 존재하지 않으면 새로 생성
            create_data = {
                'name': insta_id,
                'password': insta_pw,
                'IP': ip_address
            }

            serializer = InstaUserCreateSerializer(data=create_data)
            if serializer.is_valid():
                insta =serializer.save(create_data)
            else:
                return Response(serializer.errors, status=400)

        # Create a CustomResponse object
        response = Response(status=status.HTTP_204_NO_CONTENT)

        # Set a cookie on the response
        response.set_cookie(
            key="insta",
            value=json.dumps({"id": insta.id, "name": insta_id}),
            max_age=3600,
            httponly=True,
            secure=False,
            samesite="Lax"
            )

        return response


#
@api_view(['GET'])
def insta_image_download_api_view(request):
	now = time.time()
	is_login, code = check_insta_login(request)
	if not is_login:
		return Response(status=code)

	try:
		insta = Insta.objects.select_related().get(id=code)
		func_type = InstaFuncType.objects.get(pk=1)
	except Insta.DoesNotExist:
		return Response(status=491)
	except InstaFuncType.DoesNotExist:
		return Response(msg="Function type not found", status=500)

	history_instance = InstaHistory(type=func_type, insta=insta)

	try:
		images = post_shortcode_downloader(request.data.get('url'))
	except BadResponseException as e:
		if "Fetching Post metadata failed." == str(e):
			query = {
				"request": {
					'type': InstaFuncType.objects.get(pk=1).type,
					'url': request.data.get('url'),
					},
				"response": {
					'code': "ERROR",
					'status': 494,
					'reason': str(e)
					}
				}

			history_instance.query = query
			history_instance.save()

			return Response(status=494)

		else:
			return Response(msg=str(e), status=500)

	runtime = time.time() - now
	formatted_runtime = f"{int(runtime * 1000)} ms" if runtime < 1 else f"{round(runtime, 2)} s"

	response_data = {
		'images': images,
		'cnt': len(images),
		'runtime': formatted_runtime,
		}

	query = {
		"request": {
			'type': func_type.type,
			'url': request.data.get('url'),
			},
		"response": {
			'code': "SUCCESS",
			'status': 200,
			'cnt': len(images),
			'runtime': formatted_runtime,
			}
		}

	with transaction.atomic():
		history_instance.query = query
		history_instance.save()

	return Response(data=response_data, status=200)
