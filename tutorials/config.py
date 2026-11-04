import os
eo_service_url = "https://openeo.digitalearth.se"
user = "testuser"
passwd = "secretpassword"

eo_service_url = os.environ.get("DES_URL", eo_service_url)
user = os.environ.get("DES_USER", user)
passwd = os.environ.get("DES_PASSWORD", passwd)
