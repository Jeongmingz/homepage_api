from instaloader import LoginException
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password, check_password
from insta.models import Insta
from insta.serializers import InstaUserCreateSerializer
from share.functions import return_login_insta_instance
from utils.response import Response


class InstaUserApi(APIView):
    def post(self, request):
        insta_id = request.data.get('id')
        insta_pw = request.data.get('pw')
        ip_address = request.META.get('REMOTE_ADDR', request.META.get('HTTP_X_FORWARDED_FOR', '0,0,0,0'))

        if not insta_id or not insta_pw:
            return Response(data={'error': 'Missing id or pw'}, status=400)

        try:
            return_login_insta_instance(insta_id, insta_pw)
        except LoginException as e:
	        if 'Checkpoint required' in str(e):
		        pass
	        else:
		        return Response(
			        data=e.__str__(),
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
                serializer.save(create_data)
            else:
                return Response(serializer.errors, status=400)

        # 비밀번호 해시 값 생성

        return Response(
            status=203,
        )
