import meraki
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ.get("API_KEY")
dashboard = meraki.DashboardAPI(API_KEY, suppress_logging=True)

source_networkId = 'Source Network ID'  # Replace with the network ID to copy routes from
destination_networkId = 'Destination Network ID'  # Replace with the network ID to create routes in

def get_static_routes(network_id):
    try:
        response = dashboard.appliance.getNetworkApplianceStaticRoutes(network_id)
        static_routes = []  # Initialize an empty list to hold the route information

        for route in response:
            # Create a dictionary with the route information and append it to the list
            static_routes.append({
                'id':route['id'],
                'name': route['name'],
                'subnet': route['subnet'],
                'gatewayIp': route['gatewayIp'],
                # 'gatewayVlanId' may not be present in all routes, so we provide a default value of None
                'gatewayVlanId': route.get('gatewayVlanId', None)
            })
        return static_routes
    except meraki.APIError as e:
        print(f"Meraki API error: {e}")
        return None
    except Exception as e:
        print(f"Some other error occurred: {e}")
        return None

def create_static_routes(destination_network_id, static_routes):
    for route in static_routes:
        try:
            # Ensure 'gatewayVlanId' is not included if it's None
            route_params = {k: v for k, v in route.items() if v is not None and k != 'id'}
            response = dashboard.appliance.createNetworkApplianceStaticRoute(destination_network_id, **route_params)
            print(f"\033[1m\033[3m\033[32mSuccessfully\033[0m configured route {route['name']}: {route['subnet']}.")
        except meraki.APIError as e:
            print(f"\033[1m\033[3m\033[31mError\033[0m Meraki API error: {e}. Error with route {route['name']}: {route['subnet']}")
            # Continue to next route instead of returning None
        except Exception as e:
            print(f"\033[1m\033[3m\033[31mError\033[0m Some other error occurred: {e} With route {route['name']}: {route['subnet']}")
            # Continue to next route instead of returning None
    print("All routes have been configured.")

def main():
    static_routes = get_static_routes(source_networkId)
    if static_routes:
        create_static_routes(destination_networkId, static_routes)

if __name__ == "__main__":
    main()
