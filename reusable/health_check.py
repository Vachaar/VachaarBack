import logging
from typing import Optional, Dict
from urllib.parse import urljoin

import requests
from envparse import env

logger = logging.getLogger(__name__)


class HealthCheckBase:
    """
    A base class for managing health checks. Includes methods to build URLs, send health check requests, and handle errors.

    Attributes:
        base_url (str): The base URL for health check endpoints.
        NAME_TO_CODE_MAP (Dict[str, str]): Mapping of health check names to their corresponding codes.
        SEND_FAILED (str): Response returned when the health check fails to send.
        TIME_OUT (int): Timeout value for health check requests.
    """

    base_url: str = "https://hc-ping.com/"
    NAME_TO_CODE_MAP: Dict[str, str] = {"name": "xxx-xxx-xx-xxx-xxx"}
    SEND_FAILED: str = "send_failed"
    TIME_OUT: int = 30

    def __init__(self, raise_error_on_send: bool = False) -> None:
        """
        Initializes the HealthCheckBase.

        Args:
            raise_error_on_send (bool): Whether to raise an exception if sending a health check request fails.
        """
        self.raise_error_on_send = raise_error_on_send

    def build_url(self, path: str) -> str:
        """
        Builds a complete URL by joining the base URL with the specified path.

        Args:
            path (str): The relative path to append to the base URL.

        Returns:
            str: The complete URL.
        """
        return urljoin(self.base_url, path)

    def get_health_check_code(self, name: str) -> str:
        """
        Retrieves the health check code for the given name.

        Args:
            name (str): The name of the health check.

        Returns:
            str: The corresponding health check code.

        Raises:
            KeyError: If the name is not found in NAME_TO_CODE_MAP.
        """
        if name not in self.NAME_TO_CODE_MAP:
            logger.error(
                f"Health check name '{name}' not found in NAME_TO_CODE_MAP."
            )
            raise KeyError(f"Health check name '{name}' is not defined.")
        return self.NAME_TO_CODE_MAP[name]

    def get_health_check_url(self, name: str, success: bool = True) -> str:
        """
        Constructs the health check URL for the given name and status.

        Args:
            name (str): The name of the health check.
            success (bool): Whether the health check is successful.

        Returns:
            str: The corresponding health check URL.
        """
        url = self.build_url(self.get_health_check_code(name))
        if not success:
            url += "/fail"
        return url

    def send(
        self, name: str, success: bool, data: Optional[Dict] = None
    ) -> str:
        """
        Sends a health check request.

        Args:
            name (str): The name of the health check.
            success (bool): Whether the health check is successful.
            data (Optional[Dict]): Additional data to include in the request.

        Returns:
            str: The result of the request (response text or a failure message).

        Raises:
            Exception: If an error occurs and raise_error_on_send is True.
        """
        try:
            hc_url = self.get_health_check_url(name, success)
            payload = data or {}
            payload["is_ok"] = success
            response = requests.post(
                url=hc_url, json=payload, timeout=self.TIME_OUT
            )
            result = response.text
        except Exception as e:
            logger.error(
                f"Failed to send health check: name='{name}', success={success}, error='{repr(e)}'"
            )
            result = self.SEND_FAILED
            if self.raise_error_on_send:
                raise
        return result


class HealthCheck(HealthCheckBase):
    """
    A class derived from HealthCheckBase for additional specific health check management.

    Attributes:
        STH_TO_CHECK (str): The specific health check value to be used from environment variables.
        NAME_TO_CODE_MAP (Dict[str, str]): Mapping of health check names to their codes, customized for this class.
    """

    STH_TO_CHECK: str = env("STH_TO_CHECK", default="")
    NAME_TO_CODE_MAP: Dict[str, str] = {
        STH_TO_CHECK: STH_TO_CHECK,
    }
