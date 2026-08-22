
from __future__ import annotations
from dataclasses import dataclass
import base64,json,time

@dataclass
class Identity:
    subject:str
    issuer:str
    email:str|None=None
    groups:list|None=None
    claims:dict|None=None

class OIDCVerifier:
    """OIDC verification abstraction.

    This reference parser validates structural claims and expiry only.
    Production deployments MUST plug in issuer metadata/JWKS signature verification.
    """
    def __init__(self,issuer=None,audience=None,clock_skew=60):
        self.issuer=issuer
        self.audience=audience
        self.clock_skew=clock_skew

    @staticmethod
    def _decode_segment(seg):
        seg += "="*((4-len(seg)%4)%4)
        return json.loads(base64.urlsafe_b64decode(seg.encode()))

    def parse_unverified(self,token):
        parts=token.split(".")
        if len(parts)!=3: raise ValueError("invalid_jwt")
        return self._decode_segment(parts[1])

    def validate_claims(self,claims):
        now=time.time()
        if self.issuer and claims.get("iss")!=self.issuer: raise ValueError("issuer_mismatch")
        aud=claims.get("aud")
        if self.audience:
            ok=self.audience in aud if isinstance(aud,list) else aud==self.audience
            if not ok: raise ValueError("audience_mismatch")
        if "exp" in claims and float(claims["exp"])+self.clock_skew<now: raise ValueError("token_expired")
        if "sub" not in claims: raise ValueError("subject_missing")
        return Identity(claims["sub"],claims.get("iss",""),claims.get("email"),
                        claims.get("groups") or claims.get("roles") or [],claims)
