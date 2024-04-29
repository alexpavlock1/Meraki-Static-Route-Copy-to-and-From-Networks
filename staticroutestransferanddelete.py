import meraki
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ.get("API_KEY")
dashboard = meraki.DashboardAPI(API_KEY, suppress_logging=True)

source_networkId = 'L_660903245316621159'  # Replace with the network ID to copy routes from
destination_networkId = 'L_660903245316643598'  # Replace with the network ID to create routes in

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

def create_static_routes(destination_network_id, source_networkId, static_routes):
    successful_operations = 0  # Initialize a counter for successful operations

    for route in static_routes:
        try:
            # Exclude the 'id' from the route parameters as it's not needed for creation
            route_params = {k: v for k, v in route.items() if v is not None and k != 'id'}
            # Attempt to create a static route in the destination network
            dashboard.appliance.createNetworkApplianceStaticRoute(destination_network_id, **route_params)
            print(f"\033[1m\033[3m\033[32mSuccessfully configured route {route['name']}: {route['subnet']} to {destination_network_id}.\033[0m")

            # If the create operation was successful, attempt to delete the route from the source network
            dashboard.appliance.deleteNetworkApplianceStaticRoute(source_networkId, route['id'])
            print(f"\033[1m\033[3m\033[32mSuccessfully deleted route {route['name']}: {route['subnet']} from {source_networkId}.\033[0m")
            
            # If both operations were successful, increment the counter
            successful_operations += 1

        except meraki.APIError as e:
            print(f"\033[1m\033[3m\033[31mError: Meraki API error: {e}. Error with route {route['name']}: {route['subnet']}\033[0m")
        except Exception as e:
            print(f"\033[1m\033[3m\033[31mError: Some other error occurred: {e} With route {route['name']}: {route['subnet']}\033[0m")

    # After all routes have been processed, check if all operations were successful
    if successful_operations == len(static_routes):
        print("\033[1m\033[3m\033[32mAll routes have been successfully configured and deleted.\033[0m")
    else:
        print("\033[1m\033[3m\033[31mSome or none of the routes have been successfully configured.\033[0m")

def main():
    static_routes = get_static_routes(source_networkId)
    if static_routes:
        create_static_routes(destination_networkId, source_networkId, static_routes)

if __name__ == "__main__":
    main()
