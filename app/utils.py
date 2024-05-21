import aiohttp
import asyncio


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


def fetch_random_activity(type=None, participants=None):
    """
    Synchronously fetch an activity by running the asynchronous fetch function.

    Args:
        type (str, optional): The type of activity to fetch.
        participants (int, optional): The number of participants for the activity.

    Returns:
        dict: The JSON response from the API containing the activity details.
    """
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    async def main():
        async with aiohttp.ClientSession() as session:
            return await fetch_activity(session, type, participants)

    return loop.run_until_complete(main())
