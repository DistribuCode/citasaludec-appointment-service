from fastapi import Security, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
import os

security = HTTPBearer()

def verify_jwt(credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    print("🔥 Token recibido en middleware:", token)
    try:
        payload = jwt.decode(
            token,
            os.getenv("JWT_SECRET"),
            algorithms=["HS256"],
            leeway=60  # Permite hasta 60 segundos de diferencia de reloj
        )
        print("✅ Token decoded:", payload)
        return payload
    except jwt.ExpiredSignatureError:
        print("⛔ Token expired")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
        )
    except jwt.InvalidSignatureError as e:
        print(f"⛔ Signature verification failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid signature",
        )
    except jwt.InvalidTokenError as e:
        print(f"⛔ Invalid token reason: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
