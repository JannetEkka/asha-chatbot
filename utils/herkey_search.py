import os
import requests
import json
import random

class HerkeyJobSearch:
    """Class for simulating job searches using Gemini API."""

    def __init__(self):
        """Initialize with Gemini API key."""
        self.api_key = os.getenv("GEMINI_API_KEY", "")
        # Update to use gemini-1.5-flash model instead of gemini-pro
        self.api_url = "https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent"

        if not self.api_key:
            print("Warning: GEMINI_API_KEY environment variable not set.")

    def search_jobs(self, job_role, location=None, experience=None):
        """
        Search for jobs using Gemini API simulation.

        Args:
            job_role (str): The job role to search for
            location (str, optional): The job location
            experience (str, optional): The experience level

        Returns:
            list: A list of job dictionaries with title, company, location, etc.
        """
        if not self.api_key:
            print("No API key found - falling back to mock data")
            return self._get_mock_jobs(job_role, location, experience)

        # Create the prompt for Gemini
        location_text = f" in {location}" if location else ""
        experience_text = f" with {experience} years experience" if experience else ""

        prompt = f"""Generate 5 realistic job listings for '{job_role}' positions{location_text}{experience_text}. 

        Format the response as a JSON array of job objects with these fields:
        - title: job title
        - company: company name
        - location: job location
        - type: employment type (Full-time, Part-time, Contract, etc.)
        - posted_date: when it was posted (e.g., "2 days ago")
        - url: application URL (format as: "https://herkey.com/jobs/apply/[job-title-slug]")

        Make the listings realistic and varied. Only return the JSON with no additional text."""

        try:
            print(f"Making Gemini API request for job: {job_role}, location: {location}, experience: {experience}")
            headers = {
                "Content-Type": "application/json"
            }

            data = {
                "contents": [{"parts":[{"text": prompt}]}],
                "generationConfig": {
                    "temperature": 0.2,
                    "topP": 0.8,
                    "topK": 40
                }
            }

            url = f"{self.api_url}?key={self.api_key}"
            print(f"Sending request to Gemini API...")
            response = requests.post(url, headers=headers, json=data)

            if response.status_code == 200:
                print("Received successful response from Gemini API")
                response_json = response.json()
                text_response = response_json.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', '')

                print(f"Response content length: {len(text_response)}")

                # Extract JSON from text response
                try:
                    # Look for JSON content in the response
                    start_idx = text_response.find('[')
                    end_idx = text_response.rfind(']') + 1

                    if start_idx >= 0 and end_idx > start_idx:
                        json_str = text_response[start_idx:end_idx]
                        jobs = json.loads(json_str)
                        print(f"Successfully extracted {len(jobs)} jobs from Gemini API response")
                        return jobs
                    else:
                        print("Could not find JSON array in response - falling back to mock data")
                        return self._get_mock_jobs(job_role, location, experience)
                except json.JSONDecodeError as e:
                    print(f"JSON decode error: {e} - falling back to mock data")
                    return self._get_mock_jobs(job_role, location, experience)
            else:
                print(f"API error - status code: {response.status_code} - falling back to mock data")
                print(f"Error response: {response.text[:200]}")
                return self._get_mock_jobs(job_role, location, experience)

        except Exception as e:
            print(f"Error using Gemini API for job search: {str(e)}")
            return self._get_mock_jobs(job_role, location, experience)

    def _get_mock_jobs(self, job_role, location=None, experience=None):
        """Generate mock job data for demonstration purposes."""
        print("Generating mock job data")

        # Create a job title slug for the URL
        job_role_slug = job_role.lower().replace(' ', '-') if job_role else "job"
        location_str = location.lower() if location else "remote"

        mock_jobs = [
            {
                "title": f"Senior {job_role.title() if job_role else 'Software Developer'}",
                "company": "TechInnovate",
                "location": location or "Bangalore",
                "type": "Full-time",
                "posted_date": "3 days ago",
                "url": f"https://herkey.com/jobs/apply/{job_role_slug}-senior"
            },
            {
                "title": f"{job_role.title() if job_role else 'Data Analyst'}",
                "company": "Analytics Pro",
                "location": location or "Mumbai",
                "type": "Full-time",
                "posted_date": "1 day ago",
                "url": f"https://herkey.com/jobs/apply/{job_role_slug}"
            },
            {
                "title": f"Junior {job_role.title() if job_role else 'Web Developer'}",
                "company": "WebDesign Solutions",
                "location": location or "Remote",
                "type": "Contract",
                "posted_date": "5 days ago",
                "url": f"https://herkey.com/jobs/apply/{job_role_slug}-junior"
            },
            {
                "title": f"{job_role.title() if job_role else 'Product Manager'} Team Lead",
                "company": "InnovateTech",
                "location": location or "Delhi",
                "type": "Full-time",
                "posted_date": "2 days ago",
                "url": f"https://herkey.com/jobs/apply/{job_role_slug}-lead"
            },
            {
                "title": f"{job_role.title() if job_role else 'UX Designer'} Consultant",
                "company": "CreativeDesigns",
                "location": location or "Hyderabad",
                "type": "Part-time",
                "posted_date": "4 days ago",
                "url": f"https://herkey.com/jobs/apply/{job_role_slug}-consultant"
            }
        ]

        # Filter by location if provided
        if location:
            mock_jobs = [job for job in mock_jobs if location.lower() in job["location"].lower()]
            # If no jobs match the location, change some to match
            if not mock_jobs:
                mock_jobs = [
                    {
                        "title": f"Senior {job_role.title() if job_role else 'Software Developer'}",
                        "company": "TechInnovate",
                        "location": location,
                        "type": "Full-time",
                        "posted_date": "3 days ago",
                        "url": f"https://herkey.com/jobs/apply/{job_role_slug}-senior"
                    },
                    {
                        "title": f"Junior {job_role.title() if job_role else 'Web Developer'}",
                        "company": "WebDesign Solutions",
                        "location": location,
                        "type": "Contract",
                        "posted_date": "5 days ago",
                        "url": f"https://herkey.com/jobs/apply/{job_role_slug}-junior"
                    },
                    {
                        "title": f"{job_role.title() if job_role else 'Product Manager'} Team Lead",
                        "company": "InnovateTech",
                        "location": location,
                        "type": "Full-time",
                        "posted_date": "2 days ago",
                        "url": f"https://herkey.com/jobs/apply/{job_role_slug}-lead"
                    }
                ]

        # Only return 2-3 jobs to be more realistic
        result = random.sample(mock_jobs, min(3, len(mock_jobs)))
        print(f"Generated {len(result)} mock jobs")
        return result
