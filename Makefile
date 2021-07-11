run:
	FORWARDED_ALLOW_IPS="*" uvicorn run:app --port 8080 --host 0.0.0.0 --app-dir src