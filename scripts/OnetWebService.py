
import os
import requests
from typing import Dict, Optional, Any
from dotenv import load_dotenv


class OnetWebService:
    def __init__(self):
        """Initialize the O*NET Web Service with credentials from environment variables"""
        # Load environment variables
        load_dotenv('../env_var.env')

        # Get credentials from environment
        self.username = os.getenv('ONET_API_USERNAME')
        self.password = os.getenv('ONET_API_PASSWORD')

        if not self.username or not self.password:
            raise ValueError("Missing O*NET API credentials in environment variables. "
                           "Please set ONET_API_USERNAME and ONET_API_PASSWORD in env_var.env")

        self.base_url = "https://services.onetcenter.org/ws"
        self.headers = {
            "User-Agent": "Python/OnetWebService",
            "Accept": "application/json"  # Request JSON format
        }

    def call(self, path: str, **params) -> Optional[Dict[str, Any]]:
        """Makes a call to the O*NET Web Services API"""
        url = f"{self.base_url}/{path}"

        try:
            response = requests.get(
                url,
                params=params,
                auth=(self.username, self.password),
                headers=self.headers
            )
            response.raise_for_status()

            # Parse JSON response
            return response.json()

        except requests.exceptions.RequestException as e:
            print(f"API request error: {e}")
            return None
        except ValueError as e:  # JSON parsing error
            print(f"JSON parsing error: {e}")
            return None


def main():
    """Main function to test O*NET Web Services connection"""
    try:
        # Initialize web service
        onet = OnetWebService()

        # Test base connection
        print("\nTesting connection to O*NET Web Services...")
        response = onet.call('')

        if response:
            print("✅ Successfully connected to O*NET Web Services")
            if 'resource' in response:
                print("\nAvailable services:")
                for resource in response.get('resource', []):
                    title = resource.get('title', '(No title)')
                    href = resource.get('href', '(No URL)')
                    print(f"- {title} ({href})")

            # Try a specific service endpoint
            print("\nTesting search functionality...")
            search_response = onet.call('online/search',
                                      keyword='software developer',
                                      end=3)

            if search_response and 'occupation' in search_response:
                print("✅ Search test successful")
                print("\nExample results:")
                for occ in search_response.get('occupation', [])[:3]:
                    title = occ.get('title', '(No title)')
                    code = occ.get('code', '(No code)')
                    print(f"- {title} ({code})")
            else:
                print("❌ Search test failed")

        else:
            print("❌ Failed to connect to O*NET Web Services")

    except Exception as e:
        print(f"❌ Error during testing: {e}")


if __name__ == "__main__":
    main()