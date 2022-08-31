from twocaptcha import TwoCaptcha
import os
solver = TwoCaptcha(os.getenv("CAPTCHA_API"))
result = solver.normal('images/1.jpeg', caseSensitive = 1)
print(result);