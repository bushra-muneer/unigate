# main.py
from fastapi import FastAPI
from unigate.main import app as unigate_app
from university_stub.main import app as university_stub_app

main_app = FastAPI()

main_app.mount("/unigate", unigate_app)
main_app.mount("/university", university_stub_app)
