import aiohttp
import asyncio
import os
import random
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist

# Ensure you have your Unsplash access key stored in an environment variable
UNSPLASH_ACCESS_KEY = os.getenv('UNSPLASH_ACCESS_KEY')

# Download necessary NLTK data files
nltk.download('punkt')
nltk.download('stopwords')


def extract_keywords(activity):
    """
    Extract meaningful keywords from the activity description.

    Args:
        activity (str): The activity description.

    Returns:
        str: A space-separated string of keywords.
    """
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(activity)
    filtered_words = [
        word for word in words if word.isalnum() and word.lower() not in stop_words
    ]
    frequency_distribution = FreqDist(filtered_words)
    keywords = frequency_distribution.most_common(3)  # Get the 3 most common words
    keyword_string = ' '.join([keyword[0] for keyword in keywords])
    return keyword_string


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
    url = 'https://bored-api.appbrewery.com/filter/'
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


def pick_random_activity(activities):
    """
    Pick a random activity object from a JSON containing a bunch of activities.

    Args:
        activities (list): The list of activity objects.

    Returns:
        dict: The randomly picked activity object.
    """
    return random.choice(activities)


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
    random_activity = pick_random_activity(activity)
    keywords = extract_keywords(random_activity['activity'])
    image_url = await fetch_unsplash_image(session, keywords)
    return {
        'activity': random_activity,
        'image_url': image_url,  # Only return the small image URL
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
