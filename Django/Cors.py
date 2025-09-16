"""
🔹 What is CORS?

CORS stands for Cross-Origin Resource Sharing.

Browsers implement a security policy called Same-Origin Policy, 
which blocks web pages from making requests to a different domain than the one that served the page.

CORS is a mechanism that allows servers to whitelist other origins so that cross-domain requests are allowed.


Example

Suppose:

Your frontend runs at: http://localhost:3000

Your backend API runs at: http://localhost:8000

If the frontend tries to fetch:

fetch('http://localhost:8000/api/employees')
"""

INSTALLED_APPS = [
    'corsheaders',
]


# Allow all (not recommended for production)
CORS_ALLOW_ALL_ORIGINS = True

# Or allow specific domains
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "https://myfrontend.com",
]


"""
| Term    | Meaning                                                            |
| ------- | ------------------------------------------------------------------ |
| CORS    | Cross-Origin Resource Sharing                                      |
| Purpose | Allow frontend apps to access backend APIs from a different origin |
| How     | Server sends headers like `Access-Control-Allow-Origin` to browser |


⚡ Memory Tip:

Browser blocks cross-domain requests by default → CORS tells the browser “okay, you can trust this domain”.

Backend is in control — frontend cannot bypass CORS.
"""