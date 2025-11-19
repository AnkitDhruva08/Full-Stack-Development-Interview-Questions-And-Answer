import hmac
import hashlib

secret = "Secret-Sagmeister_1"
body = '{"event":"subscription.activated","payload":{"subscription":{"entity":{"id":"sub_1234567890abcdef","status":"active"}}}}'

signature = hmac.new(secret.encode(), body.encode(), hashlib.sha256).hexdigest()
print(signature)
