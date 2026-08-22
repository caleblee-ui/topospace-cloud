
import os
from cloud19.auth import APIKeyStore
from cloud19.rate_limit import SlidingWindowRateLimiter
from cloud19.metering import UsageMeter
from cloud19.tenant import TenantPlan
from cloud20.billing import BillingLedger
from cloud20.resilience import ResilientProviderRouter
from cloud20.fake_provider import DeterministicProvider
from cloud20.service import ExecutingTopoSpaceCloudService
from cloud21.http_provider import OpenAICompatibleHTTPProvider

def env_bool(name,default=False):
    return os.getenv(name,str(default)).lower() in {"1","true","yes","on"}

def build_service():
    tenant=os.getenv("TOPOSPACE_TENANT_ID","default")
    public_key=os.getenv("TOPOSPACE_API_KEY","")
    if not public_key:
        raise RuntimeError("TOPOSPACE_API_KEY is required")

    key_store=APIKeyStore()
    key_store.issue(tenant,public_key)

    plans={tenant:TenantPlan(
        tenant,
        requests_per_minute=int(os.getenv("TOPOSPACE_RPM","60")),
        monthly_token_limit=int(os.getenv("TOPOSPACE_MONTHLY_TOKEN_LIMIT","1000000")),
        monthly_cost_limit=float(os.getenv("TOPOSPACE_MONTHLY_COST_LIMIT","100"))
    )}

    providers={}
    primary_url=os.getenv("PRIMARY_PROVIDER_BASE_URL","").rstrip("/")
    primary_key=os.getenv("PRIMARY_PROVIDER_API_KEY","")
    if primary_url and primary_key:
        providers["primary"]=OpenAICompatibleHTTPProvider(
            primary_url,primary_key,
            provider_name=os.getenv("PRIMARY_PROVIDER_NAME","primary")
        )

    fallback_url=os.getenv("FALLBACK_PROVIDER_BASE_URL","").rstrip("/")
    fallback_key=os.getenv("FALLBACK_PROVIDER_API_KEY","")
    if fallback_url and fallback_key:
        providers["fallback"]=OpenAICompatibleHTTPProvider(
            fallback_url,fallback_key,
            provider_name=os.getenv("FALLBACK_PROVIDER_NAME","fallback")
        )

    if not providers and env_bool("ALLOW_MOCK_PROVIDER",False):
        providers["primary"]=DeterministicProvider("mock")

    router=ResilientProviderRouter(
        providers,
        retries=int(os.getenv("PROVIDER_RETRIES","1"))
    ) if providers else None

    return ExecutingTopoSpaceCloudService(
        key_store,SlidingWindowRateLimiter(),UsageMeter(),plans,
        provider_router=router,billing=BillingLedger(),
        default_provider="primary" if "primary" in providers else (next(iter(providers)) if providers else "primary")
    )
