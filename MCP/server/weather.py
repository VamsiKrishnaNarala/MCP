from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("weather")

# Constants
NWS_API_BASE = "https://api.weather.gov"
USER_AGENT = "weather-app/1.0"


async def make_nws_request(url: str) -> dict[str, Any] | None:
    """Make a request to the NWS API with proper error handling."""
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/geo+json"
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None
        
def format_alert(feature: dict) -> str:
    """Format an alert feature into a readable string."""
    props = feature["properties"]
    return f"""
        Event: {props.get('event', 'Unknown')}
        Area: {props.get('areaDesc', 'Unknown')}
        Severity: {props.get('severity', 'Unknown')}
        Description: {props.get('description', 'No description available')}
        Instructions: {props.get('instruction', 'No specific instructions provided')}
        """

@mcp.tool()
async def get_alerts(state: str) -> str:
    """Get weather alerts for a US state.

    Args:
        state: Two-letter US state code (e.g. CA, NY)
    """
    url = f"{NWS_API_BASE}/alerts/active/area/{state}"
    data = await make_nws_request(url)

    if not data or "features" not in data:
        return "Unable to fetch alerts or no alerts found."

    if not data["features"]:
        return "No active alerts for this state."

    alerts = [format_alert(feature) for feature in data["features"]]
    return "\n---\n".join(alerts)

@mcp.tool()
async def get_north_america_alerts() -> str:
    """Get weather alerts for major regions in North America."""
    # List of major US states and Canadian provinces
    regions = [
        # US States
        "CA", "TX", "FL", "NY", "IL", "PA", "OH", "GA", "NC", "MI",
        # Canadian Provinces
        "BC", "AB", "ON", "QC", "NS", "NB", "MB", "SK", "NL", "PE"
    ]
    
    all_alerts = []
    for region in regions:
        url = f"{NWS_API_BASE}/alerts/active/area/{region}"
        data = await make_nws_request(url)
        
        if data and "features" in data and data["features"]:
            alerts = [format_alert(feature) for feature in data["features"]]
            all_alerts.extend(alerts)
    
    if not all_alerts:
        return "No active alerts found in North America."
    
    return "\n---\n".join(all_alerts)

@mcp.resource("echo://{message}")
def echo_resource(message: str) -> str:
    """Echo a message as a resource"""
    return f"Resource echo: {message}"