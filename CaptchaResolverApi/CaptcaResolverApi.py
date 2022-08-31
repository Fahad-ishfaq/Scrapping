from twocaptcha import TwoCaptcha
import os
solver = TwoCaptcha(os.getenv("CAPTCHA_API"))
type = "normal"

if (type == "normal"):
    print("Solving normal captcha")
    result = solver.normal('images/1.jpeg', caseSensitive = 1)
    print(result);
else:
    print("Solving Recaptcha2")
    # =============== ReCaptcha 2 =========================== #
    recaptcha2 = solver.recaptcha(sitekey='6Lc7cyAaAAAAAGUwpzByQGxfnK1A-BOPfOzuQCA2', 
                                    url='https://demo.whoisfreaks.com/live')
    print(recaptcha2)