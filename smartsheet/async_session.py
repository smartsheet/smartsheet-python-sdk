# pylint: disable=E0401,W0221,W0613
# Smartsheet Python SDK.
#
# Copyright 2016 Smartsheet.com, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"): you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

"""Async session management for Smartsheet API.

This module provides async HTTP client configuration with the same SSL/TLS
security settings as the synchronous session module. It uses httpx.AsyncClient
to provide non-blocking HTTP operations suitable for async/await patterns.
"""

# pylint: disable=no-member
# known issue regarding ssl module and pylint.

import ssl
from typing import Optional

import certifi
import httpx

_TRUSTED_CERT_FILE = certifi.where()


def _create_ssl_context() -> ssl.SSLContext:
    """Create SSL context with secure TLS configuration.
    
    Configures SSL context to:
    - Disable SSLv2, SSLv3, and TLSv1 (insecure protocols)
    - Use system default security settings
    - Verify certificates against trusted CA bundle
    
    Returns:
        ssl.SSLContext: Configured SSL context for secure connections
    """
    ctx = ssl.create_default_context()
    ctx.options |= ssl.OP_NO_SSLv2
    ctx.options |= ssl.OP_NO_SSLv3
    ctx.options |= ssl.OP_NO_TLSv1
    return ctx


def async_pinned_session(
    pool_maxsize: int = 8,
    max_retries: int = 1,
    timeout: Optional[float] = None
) -> httpx.AsyncClient:
    """Create an async HTTP client with pinned SSL/TLS configuration.
    
    This function creates an httpx.AsyncClient configured with:
    - Secure SSL/TLS settings (no SSLv2, SSLv3, or TLSv1)
    - Connection pooling for efficient resource usage
    - Automatic retry logic for transient failures
    - Certificate verification against trusted CA bundle
    
    The client should be used as an async context manager to ensure
    proper resource cleanup:
    
        async with async_pinned_session() as client:
            response = await client.get("https://api.smartsheet.com/...")
    
    Or with explicit lifecycle management:
    
        client = async_pinned_session()
        try:
            response = await client.get("https://api.smartsheet.com/...")
        finally:
            await client.aclose()
    
    Args:
        pool_maxsize: Maximum number of connections to pool (default: 8)
        max_retries: Number of retry attempts for failed requests (default: 1)
        timeout: Request timeout in seconds (default: None for no timeout)
    
    Returns:
        httpx.AsyncClient: Configured async HTTP client with secure settings
    
    Example:
        >>> async with async_pinned_session() as client:
        ...     response = await client.get("https://api.smartsheet.com/2.0/users/me")
        ...     print(response.status_code)
        200
    """
    # Create SSL context with secure configuration
    ssl_context = _create_ssl_context()
    
    # Configure connection limits for pooling
    limits = httpx.Limits(
        max_connections=pool_maxsize,
        max_keepalive_connections=pool_maxsize // 2
    )
    
    # Configure retry transport
    transport = httpx.AsyncHTTPTransport(
        limits=limits,
        verify=ssl_context,
        retries=max_retries
    )
    
    # Create async client with configuration
    client = httpx.AsyncClient(
        transport=transport,
        timeout=timeout,
        verify=_TRUSTED_CERT_FILE,
        event_hooks={
            'response': [_redact_token_async]
        }
    )
    
    return client


async def _redact_token_async(response: httpx.Response) -> None:
    """Redact authorization token from request headers for security.
    
    This hook is called after each response to remove sensitive authorization
    tokens from the request object, preventing them from appearing in logs
    or debug output.
    
    Args:
        response: The HTTP response object containing the request
    """
    if "Authorization" in response.request.headers:
        # Create new headers dict with redacted token
        response.request.headers = httpx.Headers({
            **response.request.headers,
            "Authorization": "[redacted]"
        })
