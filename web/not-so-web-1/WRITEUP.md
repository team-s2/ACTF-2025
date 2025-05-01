# Writeup - not-so-web-1

This challenge aims to *investigate cookie forgery*.
Since the `IV` is controllable, hence the username can be changed to `admin` through CBC XOR flipping to log in.

https://cryptohack.org/courses/symmetric/flipping_cookie

After that, simply searching python flask SSTI can get so many effective payloads to achieve RCE.

> It is worth mentioning that during the test, it was found that some unfiltered keywords like `eval` seemed to be blocked. I guess it was caused by the firewall of the tournament server.

The difficulty of this question is basically enough for anyone with a little experience to solve it. The core purpose is to throw a smoke bomb for the second question.