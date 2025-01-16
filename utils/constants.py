class SystemCodeManager:

	CODE_MESSAGES = {
		200: {
			"code": "SUCCESS",
			"link": None,
			"message": "정상 처리되었습니다."
			},
		201: {
			"code": "SUCCESS",
			"link": None,
			"message": "정상적으로 생성되었습니다."
			},
		203: {
			"code": "LOGIN_SUCCESS",
			"link": None,
			"message": "로그인 완료."
			},
		204: {
			"code": "NO_CONTENT",
			"link": None,
			"message": "정상적으로 삭제되었습니다."
			},
		400: {
			"code": "CLIENT ERROR",
			"link": None,
			"message": "오류가 발생했습니다."
			},
		401: {
			"code": "UNAUTHORIZED",
			"link": "/login",
			"message": "로그인이 필요합니다."
			},
		403: {
			"code": "FORBIDDEN",
			"link": "/login",
			"message": "로그인이 필요합니다."
			},
		404: {
			"code": "NOT_FOUND",
			"link": None,
			"message": "요청하신 리소스를 찾을 수 없습니다."
			},
		490: {
			"code": "INSTA_LOGIN_FAILED",
			"link": None,
			"message": "인스타그램 로그인 실패. 아이디와 비밀번호를 확인하세요."
			},
		491: {
			"code": "INSTA_UNAUTHORIZED",
			"link": None,
			"message": "인스타그램 로그인을 해주세요."
			},
		494: {
			"code": "INSTA_POST_URL_ERROR",
			"link": None,
			"message": "POST URL이 유효하지 않습니다."
			}
		}

	@classmethod
	def get_message(cls, key: int, default: str = None) -> str:
		item = cls.CODE_MESSAGES.get(key)
		if item is not None:
			return item["message"]
		return default or f"Unknown key: {key}"

	@classmethod
	def get_code(cls, key: int, default: str = None) -> str:
		item = cls.CODE_MESSAGES.get(key)
		if item is not None:
			return item["code"]
		return default or f"UNKNOWN_CODE_{key}"

	@classmethod
	def get_link(cls, key: int, default: str = None) -> str:
		item = cls.CODE_MESSAGES.get(key)
		if item is not None:
			return item["link"]
		return default or f"UNKNOWN_CODE_{key}"
