#!/usr/bin/env python3
"""
Coursera GraphQL API Example

This script demonstrates a working example of how to query Coursera's API
to search for courses and extract useful information.
"""

import requests
import json
import argparse
from typing import Dict, List, Any, Optional


class CourseraAPI:
    """Client for interacting with Coursera's APIs"""
    
    def __init__(self):
        self.base_url = "https://www.coursera.org"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

    def autocomplete_search(self, query: str, limit: int = 10) -> Dict[str, Any]:
        """
        Use Coursera's autocomplete API to search for courses, specializations, etc.
        This is a simpler, more reliable API endpoint than the GraphQL API.
        
        Args:
            query: Search term
            limit: Maximum number of results to return
            
        Returns:
            Dict containing search results
        """
        endpoint = f"{self.base_url}/api/autocomplete.v2"
        params = {
            "q": query,
            "context": "search",
            "limit": str(limit),
        }
        
        response = requests.get(endpoint, params=params, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error {response.status_code}: {response.text}")

    def graphql_search(self, query: str, limit: int = 10) -> Dict[str, Any]:
        """
        Attempt to use Coursera's GraphQL API for search
        Note: This may require authentication or special headers to work reliably
        
        Args:
            query: Search term
            limit: Maximum number of results to return
            
        Returns:
            Dict containing search results or error information
        """
        endpoint = f"{self.base_url}/graphqlBatch"
        
        # Corrected GraphQL query based on API error messages
        payload = [{
            "operationName": "ProductSearch",
            "variables": {
                "query": query,
                "start": 0,
                "limit": limit,
                "filters": {}
            },
            "query": """
            query ProductSearch($query: String!, $start: Int!, $limit: Int!, $filters: CoursesFilters) {
              CatalogResultsV2(query: $query, start: $start, limit: $limit, filters: $filters) {
                numResults
                results {
                  ... on Course {
                    courseId: id
                    name
                    description
                    partners {
                      name
                    }
                    duration
                    rating
                  }
                }
              }
            }
            """
        }]
        
        response = requests.post(endpoint, headers=self.headers, data=json.dumps(payload))
        return {
            "status_code": response.status_code,
            "response": response.json() if response.status_code == 200 else response.text
        }

    def browse_courses(self, topic: str = "data-science", limit: int = 10) -> Dict[str, Any]:
        """
        Use Coursera's browse API to get courses by topic
        This is a RESTful API endpoint that's more reliable than GraphQL for basic browsing
        
        Args:
            topic: Topic slug (e.g., 'data-science', 'machine-learning')
            limit: Maximum number of results to return
            
        Returns:
            Dict containing browse results
        """
        endpoint = f"{self.base_url}/api/browse/v1/{topic}"
        params = {
            "start": "0",
            "limit": str(limit),
            "fields": "name,slug,description,partners,skills",
        }
        
        response = requests.get(endpoint, params=params, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error {response.status_code}: {response.text}")


def display_results(data: Dict[str, Any], result_type: str) -> None:
    """
    Pretty print search results
    
    Args:
        data: API response data
        result_type: Type of results (autocomplete, graphql, browse)
    """
    print(f"\n===== {result_type.upper()} RESULTS =====\n")
    
    if result_type == "autocomplete":
        if "courses" in data:
            for i, course in enumerate(data["courses"][:10], 1):
                print(f"{i}. {course.get('name')} ({course.get('domainId')})")
                print(f"   URL: https://www.coursera.org/learn/{course.get('domainId')}")
                print(f"   Provider: {course.get('partnerName', 'Unknown')}")
                print()
        else:
            print("No courses found in autocomplete results")
    
    elif result_type == "graphql":
        if data["status_code"] == 200:
            try:
                results = data["response"][0]["data"]["CatalogResultsV2"]["results"]
                for i, course in enumerate(results[:10], 1):
                    print(f"{i}. {course.get('name')}")
                    print(f"   ID: {course.get('courseId')}")
                    print(f"   Duration: {course.get('duration', 'Not specified')}")
                    partners = [p["name"] for p in course.get("partners", [])]
                    print(f"   Provider: {', '.join(partners)}")
                    print(f"   Rating: {course.get('rating', 'Not rated')}")
                    print()
            except (KeyError, IndexError) as e:
                print(f"Unable to parse GraphQL results: {e}")
                print("Raw response:")
                print(json.dumps(data["response"], indent=2))
        else:
            print(f"GraphQL request failed with status code: {data['status_code']}")
            print(f"Error: {data['response']}")
    
    elif result_type == "browse":
        if "elements" in data:
            for i, course in enumerate(data["elements"][:10], 1):
                print(f"{i}. {course.get('name')}")
                print(f"   URL: https://www.coursera.org/learn/{course.get('slug')}")
                partners = [p["name"] for p in course.get("partners", [])]
                print(f"   Provider: {', '.join(partners)}")
                skills = [s["name"] for s in course.get("skills", [])]
                print(f"   Skills: {', '.join(skills[:3])}{'...' if len(skills) > 3 else ''}")
                print()
        else:
            print("No courses found in browse results")


def save_results(data: Dict[str, Any], filename: str) -> None:
    """
    Save API response to a JSON file
    
    Args:
        data: API response data
        filename: Output filename
    """
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Results saved to {filename}")


def main() -> None:
    """Main entry point for the script"""
    parser = argparse.ArgumentParser(description="Search Coursera for courses using different API methods")
    parser.add_argument("--query", type=str, default="python programming", 
                       help="Search query (default: 'python programming')")
    parser.add_argument("--limit", type=int, default=10,
                       help="Maximum number of results to return (default: 10)")
    parser.add_argument("--topic", type=str, default="data-science",
                       help="Topic for browse API (default: 'data-science')")
    parser.add_argument("--output", type=str, default="",
                       help="Save results to specified JSON file")
    
    args = parser.parse_args()
    client = CourseraAPI()
    
    # Method 1: Search using autocomplete API (most reliable)
    print(f"Searching Coursera for '{args.query}' using autocomplete API...")
    autocomplete_results = client.autocomplete_search(args.query, args.limit)
    display_results(autocomplete_results, "autocomplete")
    
    # Method 2: Search using GraphQL API (may not work without authentication)
    print(f"Searching Coursera for '{args.query}' using GraphQL API...")
    graphql_results = client.graphql_search(args.query, args.limit)
    display_results(graphql_results, "graphql")
    
    # Method 3: Browse courses by topic
    print(f"Browsing Coursera courses in '{args.topic}'...")
    browse_results = client.browse_courses(args.topic, args.limit)
    display_results(browse_results, "browse")
    
    # Save results if output file is specified
    if args.output:
        combined_results = {
            "autocomplete": autocomplete_results,
            "graphql": graphql_results,
            "browse": browse_results
        }
        save_results(combined_results, args.output)


if __name__ == "__main__":
    main()