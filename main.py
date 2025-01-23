import asyncio
import os
import json
from linkedin_api import Linkedin
import aiohttp

# Function to fetch profiles based on location
async def fetch_profiles_by_location(api, location):
    # Assuming we can use the search method to get profiles (location-based)
    search_results = api.search_people(keywords=location)
    profiles = []
    
    for profile in search_results:
        profile_id = profile.get('publicIdentifier')
        profile_data = await fetch_profile_data(api, profile_id)
        profiles.append(profile_data)
    
    return profiles

# Function to fetch individual profile data
async def fetch_profile_data(api, profile_id):
    # Fetch complete profile data for each profile
    profile_data = api.get_profile(profile_id)
    return profile_data

# Function to save profiles in JSON files
async def save_profiles(profiles, location):
    # Create the folder named "LinkedIn ([Location])"
    folder_path = f"LinkedIn ({location})"
    os.makedirs(folder_path, exist_ok=True)

    for profile in profiles:
        # Save each profile as a separate JSON file
        profile_filename = f"{folder_path}/{profile['firstName']}_{profile['lastName']}_profile.json"
        with open(profile_filename, 'w') as f:
            json.dump(profile, f, indent=4)

# Asynchronous main function
async def main():
    location = input("Enter the location to search profiles (e.g., Pontefract): ")
    
    # Set up LinkedIn API
    api = Linkedin('your_email@example.com', 'your_password')
    
    # Fetch profiles by location
    profiles = await fetch_profiles_by_location(api, location)
    
    # Save profiles to folder
    await save_profiles(profiles, location)
    
    print(f"Profiles saved in folder: LinkedIn ({location})")

# Run the asyncio loop
if __name__ == "__main__":
    asyncio.run(main())
