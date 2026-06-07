import os

# 🔐 ساده‌ترین سیستم لاگین (برای شروع پروژه)
ADMIN_USER = "admin"
ADMIN_PASS = "1234"


def login(username, password):
    if username == ADMIN_USER and password == ADMIN_PASS:
        return True
    return False
