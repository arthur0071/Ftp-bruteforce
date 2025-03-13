import time

key = 12931
user = "Admin"
print(f"{time.strftime('%d/%m/%y %H:%M:%S')} \033[31mFailed\033[0m to login with user: {user} and password:{key}")