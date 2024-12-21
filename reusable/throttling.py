from typing import Optional

from django.http import HttpRequest
from rest_framework.settings import api_settings
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle


def get_ident_from_headers(
    request: HttpRequest, header_name: str
) -> Optional[str]:
    """
    Retrieve the IP address from a specific HTTP header if it exists.

    Args:
        request (HttpRequest): The incoming HTTP request object.
        header_name (str): Name of the HTTP header to retrieve the IP from.

    Returns:
        Optional[str]: IP address if the header exists, otherwise None.
    """
    return request.META.get(header_name)


def parse_client_ip(request: HttpRequest) -> str:
    """
    Determine the IP of the client making the request by sequentially checking:

    1. HTTP_CF_CONNECTING_IP (Cloudflare).
    2. HTTP_AR_REAL_IP (Arvan).
    3. HTTP_X_FORWARDED_FOR (forwarded addresses, proxy aware).
    4. REMOTE_ADDR (fallback to remote address).

    The method honors `NUM_PROXIES` from REST framework settings to account for trusted proxies.

    Args:
        request (HttpRequest): The incoming HTTP request object.

    Returns:
        str: The identified IP address of the client making the request.
    """
    # Check Cloudflare and Arvan headers
    cloudflare_ip = get_ident_from_headers(request, "HTTP_CF_CONNECTING_IP")
    if cloudflare_ip:
        return cloudflare_ip

    arvan_ip = get_ident_from_headers(request, "HTTP_AR_REAL_IP")
    if arvan_ip:
        return arvan_ip

    # Check X-Forwarded-For and fallback to REMOTE_ADDR
    forwarded_for = get_ident_from_headers(request, "HTTP_X_FORWARDED_FOR")
    remote_addr = get_ident_from_headers(request, "REMOTE_ADDR")
    num_proxies = api_settings.NUM_PROXIES

    if num_proxies is not None:
        if num_proxies == 0 or not forwarded_for:
            return remote_addr or ""
        # Extract the client IP from the trusted proxy chain
        forwarded_addresses = forwarded_for.split(",")
        client_ip = forwarded_addresses[
            -min(num_proxies, len(forwarded_addresses))
        ]
        return client_ip.strip() if client_ip else ""

    # Use entire X-Forwarded-For or default to REMOTE_ADDR
    return (
        "".join(forwarded_for.split()) if forwarded_for else remote_addr or ""
    )


class BaseThrottleMixin:
    """
    Mixin to provide `get_ident` functionality for throttling classes.
    Subclasses need to override `get_ident` as required.
    """

    def get_ident(self, request: HttpRequest) -> str:
        """
        Retrieve the client identifier for throttling.

        Args:
            request (HttpRequest): The incoming HTTP request object.

        Returns:
            str: Identifier derived from the request.
        """
        return parse_client_ip(request)


class CDNUserRateThrottle(BaseThrottleMixin, UserRateThrottle):
    """
    User rate throttle using client identification based on CDN headers.
    """


class CDNAnonRateThrottle(BaseThrottleMixin, AnonRateThrottle):
    """
    Anonymous rate throttle using client identification based on CDN headers.
    """


class CDNExclusiveAnonRateThrottle(BaseThrottleMixin, AnonRateThrottle):
    """
    Anonymous rate throttling with a mechanism to exclude specific IPs.
    """

    exclude_ips: list[str] = []

    def get_cache_key(self, request: HttpRequest, view) -> Optional[str]:
        """
        Generate the cache key for throttling, excluding certain IPs.

        Args:
            request (HttpRequest): The incoming HTTP request object.
            view: The view being accessed.

        Returns:
            Optional[str]: Cache key or None if the request should not be throttled.
        """
        if request.user.is_authenticated:
            return None  # Authenticated users are not throttled.

        ident = self.get_ident(request)
        if ident in self.exclude_ips:
            return None

        return self.cache_format % {"scope": self.scope, "ident": ident}


class CFUserRateThrottle(BaseThrottleMixin, UserRateThrottle):
    """
    User rate throttle using client identification specific to Cloudflare CDN.
    """

    def get_ident(self, request: HttpRequest) -> str:
        """
        Override the get_ident to specifically identify clients based on Cloudflare headers.

        Args:
            request (HttpRequest): The incoming HTTP request object.

        Returns:
            str: Identifier derived using Cloudflare headers.
        """
        cf_ip = get_ident_from_headers(request, "HTTP_CF_CONNECTING_IP")
        if cf_ip:
            return cf_ip
        return parse_client_ip(request)


class CFAnonRateThrottle(BaseThrottleMixin, AnonRateThrottle):
    """
    Anonymous rate throttle using client identification specific to Cloudflare CDN.
    """

    def get_ident(self, request: HttpRequest) -> str:
        """
        Override the get_ident to specifically identify clients based on Cloudflare headers.

        Args:
            request (HttpRequest): The incoming HTTP request object.

        Returns:
            str: Identifier derived using Cloudflare headers.
        """
        cf_ip = get_ident_from_headers(request, "HTTP_CF_CONNECTING_IP")
        if cf_ip:
            return cf_ip
        return parse_client_ip(request)
