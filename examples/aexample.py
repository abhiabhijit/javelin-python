import asyncio
import json

from javelin_sdk import (
    JavelinClient,
    Route,
    NetworkError,
    RouteNotFoundError,
    UnauthorizedError,
)


def pretty_print(obj):
    """
    Pretty-prints an object that has a JSON representation.
    """
    if hasattr(obj, "dict"):
        obj = obj.dict()

    print(json.dumps(obj, indent=4))


async def main():
    print("Javelin Asynchronous Example Code")
    """
    Create a JavelinClient object. This object is used to interact
    with the Javelin API. The base_url parameter is the URL of the Javelin API. 
    This is usually http://localhost:8000 if you are running Javelin locally.
    """
    try:
        client = JavelinClient(base_url="http://localhost:8000")
    except NetworkError as e:
        print("Failed to create client: Network Error")
        return

    """
    Start the example by cleaning up any pre-existing routes. 
    This is done by deleting the route if it exists.
    """
    print("1. Start clean (by deleting pre-existing routes): ", "test_route_1")
    try:
        await client.adelete_route("test_route_1")
    except UnauthorizedError as e:
        print("Failed to delete route: Unauthorized")
    except NetworkError as e:
        print("Failed to delete route: Network Error")
    except RouteNotFoundError as e:
        print("Failed to delete route: Route Not Found")

    """
    Create a route. This is done by creating a Route object and passing it to the
    create_route method of the JavelinClient object.
    """
    route_data = {
        "name": "test_route_1",
        "type": "chat",
        "model": {
            "name": "gpt-3.5-turbo",
            "provider": "openai",
            "suffix": "/chat/completions",
        },
        "config": {
            "archive": True,
            "organization": "myusers",
            "retries": 3,
            "rate_limit": 7,
        },
    }
    route = Route.parse_obj(route_data)
    pretty_print("2. Creating route: ", route.name)
    try:
        await client.acreate_route(route)
    except UnauthorizedError as e:
        print("Failed to create route: Unauthorized")
    except NetworkError as e:
        print("Failed to create route: Network Error")

    """
    Query the route. This is done by calling the query_route method of the JavelinClient
    object. The query data is passed as a dictionary. The keys of the dictionary are the
    same as the fields of the QueryRequest object. The values of the dictionary are the
    same as the fields of the Message object.
    """
    query_data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello!"},
        ],
        "temperature": 0.8,
    }

    print("3. Querying route: ", route.name)
    try:
        response = await client.aquery_route("test_route_1", query_data)
        pretty_print(response)
    except UnauthorizedError as e:
        print("Failed to query route: Unauthorized")
    except NetworkError as e:
        print("Failed to query route: Network Error")
    except RouteNotFoundError as e:
        print("Failed to query route: Route Not Found")

    """
    List routes. This is done by calling the list_routes method of the JavelinClient object.
    """
    print("4. Listing routes")
    try:
        pretty_print(await client.alist_routes())
    except UnauthorizedError as e:
        print("Failed to list routes: Unauthorized")
    except NetworkError as e:
        print("Failed to list routes: Network Error")

    print("5. Get Route: ", route.name)
    try:
        pretty_print(await client.aget_route(route.name))
    except UnauthorizedError as e:
        print("Failed to get route: Unauthorized")
    except NetworkError as e:
        print("Failed to get route: Network Error")
    except RouteNotFoundError as e:
        print("Failed to get route: Route Not Found")

    """
    Update the route. This is done by calling the update_route method of the JavelinClient
    object. The route object is passed as an argument.
    """
    print("6. Updating Route: ", route.name)
    try:
        route.config.retries = 5
        await client.aupdate_route(route)
    except UnauthorizedError as e:
        print("Failed to update route: Unauthorized")
    except NetworkError as e:
        print("Failed to update route: Network Error")
    except RouteNotFoundError as e:
        print("Failed to update route: Route Not Found")

    """
    Get the route. This is done by calling the get_route method of the JavelinClient object.
    """
    print("7. Get Route: ", route.name)
    try:
        pretty_print(await client.aget_route(route.name))
    except UnauthorizedError as e:
        print("Failed to get route: Unauthorized")
    except NetworkError as e:
        print("Failed to get route: Network Error")
    except RouteNotFoundError as e:
        print("Failed to get route: Route Not Found")

    """
    Delete the route. This is done by calling the delete_route method of the JavelinClient
    object.
    """
    print("8. Deleting Route: ", route.name)
    try:
        await client.adelete_route(route.name)
    except UnauthorizedError as e:
        print("Failed to delete route: Unauthorized")
    except NetworkError as e:
        print("Failed to delete route: Network Error")
    except RouteNotFoundError as e:
        print("Failed to delete route: Route Not Found")


if __name__ == "__main__":
    asyncio.run(main())
