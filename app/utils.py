import aiohttp
import asyncio
import os

# Ensure you have your Unsplash access key stored in an environment variable
UNSPLASH_ACCESS_KEY = os.getenv('UNSPLASH_ACCESS_KEY')


async def fetch_activity(session, type=None, participants=None):
    """
    Asynchronously fetch an activity from the Bored API.

    Args:
        session (aiohttp.ClientSession): The HTTP client session.
        type (str, optional): The type of activity to fetch.
        participants (int, optional): The number of participants for the activity.

    Returns:
        dict: The JSON response from the API containing the activity details.
    """
    url = 'http://www.boredapi.com/api/activity/'
    params = {}
    if type:
        params['type'] = type
    if participants:
        params['participants'] = participants

    async with session.get(url, params=params) as response:
        return await response.json()


async def fetch_unsplash_image(session, query):
    """
    Asynchronously fetch a random image from Unsplash based on a query.

    Args:
        session (aiohttp.ClientSession): The HTTP client session.
        query (str): The search query for fetching the image.

    Returns:
        dict: The JSON response from the Unsplash API containing the image details.
    """
    url = 'https://api.unsplash.com/photos/random'
    params = {'query': query, 'orientation': 'landscape', 'count': 1}
    headers = {'Authorization': f'Client-ID {UNSPLASH_ACCESS_KEY}'}

    async with session.get(url, params=params, headers=headers) as response:
        json_response = await response.json()
        if json_response and isinstance(json_response, list) and len(json_response) > 0:
            return json_response[0]['urls']['small']
        return None


async def fetch_activity_and_image(session, type=None, participants=None):
    """
    Asynchronously fetch an activity and its related image.

    Args:
        session (aiohttp.ClientSession): The HTTP client session.
        type (str, optional): The type of activity to fetch.
        participants (int, optional): The number of participants for the activity.

    Returns:
        dict: The combined response containing activity and image details.
    """
    activity = await fetch_activity(session, type, participants)
    image_url = await fetch_unsplash_image(session, activity['activity'])
    return {
        'activity': activity,
        'image_url': image_url  # Only return the small image URL
    }


def fetch_random_activity(type=None, participants=None):
    """
    Synchronously fetch an activity by running the asynchronous fetch function.

    Args:
        type (str, optional): The type of activity to fetch.
        participants (int, optional): The number of participants for the activity.

    Returns:
        dict: The combined response containing activity and image details.
    """
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    async def main():
        async with aiohttp.ClientSession() as session:
            return await fetch_activity_and_image(session, type, participants)

    return loop.run_until_complete(main())
