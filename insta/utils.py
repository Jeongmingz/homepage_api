from insta.models import Insta
import json


def check_insta_login(request) -> (bool, int):
	"""
	유저의 cookie에 insta login이 존재하는지의 여부를 판단.

	존재하지 않을 경우, Custom Error code인 491 return
	존재할 경우, 해당 insta model의 id값 return
	"""

	value = request.COOKIES.get('insta')

	value = json.loads(value)

	if value is None:
		return False, 491

	insta = Insta.objects.get(
		pk=value.get('id'),
		name=value.get('name'),
		)

	return True, insta.pk
