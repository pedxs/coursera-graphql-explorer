#!/usr/bin/env python3
"""
Coursera GraphQL API Example

This script demonstrates how to query Coursera's GraphQL API
and includes multiple query examples to explore the available schema.
"""

import requests
import json
import argparse
from typing import Dict, List, Any, Optional


class CourseraGraphQLClient:
    """Client for interacting with Coursera's GraphQL API"""
    
    def __init__(self, debug: bool = False):
        """
        Initialize the GraphQL client
        
        Args:
            debug: Enable debug mode for verbose logging
        """
        self.base_url = "https://www.coursera.org"
        self.graphql_endpoint = f"{self.base_url}/graphqlBatch"
        self.debug = debug
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-Requested-With": "XMLHttpRequest",
            "Origin": "https://www.coursera.org",
            "Referer": "https://www.coursera.org/search"
        }
    
    def execute_query(self, operation_name: str, query: str, variables: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a GraphQL query
        
        Args:
            operation_name: Name of the GraphQL operation
            query: GraphQL query string
            variables: Variables to include in the query
            
        Returns:
            Dict containing the GraphQL response or error information
        """
        payload = [{
            "operationName": operation_name,
            "variables": variables,
            "query": query
        }]
        
        if self.debug:
            print(f"GraphQL Request to {self.graphql_endpoint}:")
            print(f"Operation: {operation_name}")
            print(f"Variables: {json.dumps(variables, indent=2)}")
            print(f"Query: {query}")
        
        response = requests.post(self.graphql_endpoint, headers=self.headers, data=json.dumps(payload))
        
        if self.debug:
            print(f"Response Status: {response.status_code}")
            print(f"Response Headers: {json.dumps(dict(response.headers), indent=2)}")
        
        return {
            "status_code": response.status_code,
            "response": response.json() if response.status_code == 200 else response.text
        }
    
    def search_courses(self, query: str, limit: int = 10) -> Dict[str, Any]:
        """
        Search for courses using Coursera's GraphQL API
        
        Args:
            query: Search term
            limit: Maximum number of results to return
            
        Returns:
            Dict containing search results or error information
        """
        operation_name = "CourseSearch"
        graphql_query = """
        query CourseSearch($query: String!, $start: Int!, $limit: Int!, $filters: CoursesFilters) {
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
        
        variables = {
            "query": query,
            "start": 0,
            "limit": limit,
            "filters": {}
        }
        
        return self.execute_query(operation_name, graphql_query, variables)
    
    def get_course_info(self, course_id: str) -> Dict[str, Any]:
        """
        Get detailed information about a specific course
        
        Args:
            course_id: The course ID
            
        Returns:
            Dict containing course details or error information
        """
        operation_name = "CourseInfo"
        graphql_query = """
        query CourseInfo($courseId: String!) {
          Course(id: $courseId) {
            id
            name
            slug
            description
            instructors {
              fullName
              title
            }
            partners {
              name
              logoUrl
            }
            enrollment {
              availableSessions {
                startDate
                endDate
              }
            }
          }
        }
        """
        
        variables = {
            "courseId": course_id
        }
        
        return self.execute_query(operation_name, graphql_query, variables)
    
    def search_specializations(self, query: str, limit: int = 10) -> Dict[str, Any]:
        """
        Search for specializations using Coursera's GraphQL API
        
        Args:
            query: Search term
            limit: Maximum number of results to return
            
        Returns:
            Dict containing search results or error information
        """
        operation_name = "SpecializationSearch"
        graphql_query = """
        query SpecializationSearch($query: String!, $start: Int!, $limit: Int!) {
          SpecializationResultsV2(query: $query, start: $start, limit: $limit) {
            total
            elements {
              id
              name
              slug
              description
              partners {
                name
              }
              courses {
                name
                slug
              }
            }
          }
        }
        """
        
        variables = {
            "query": query,
            "start": 0,
            "limit": limit
        }
        
        return self.execute_query(operation_name, graphql_query, variables)


def display_results(data: Dict[str, Any], query_type: str) -> None:
    """
    Pretty print GraphQL query results
    
    Args:
        data: API response data
        query_type: Type of GraphQL query (courses, course_info, specializations)
    """
    print(f"\n===== {query_type.upper()} QUERY RESULTS =====\n")
    
    if data["status_code"] != 200:
        print(f"GraphQL request failed with status code: {data['status_code']}")
        print(f"Error: {data['response']}")
        return
    
    try:
        if query_type == "courses":
            # Handle course search results
            results = data["response"][0]["data"]["CatalogResultsV2"]["results"]
            total = data["response"][0]["data"]["CatalogResultsV2"]["numResults"]
            
            print(f"Found {total} courses matching your query\n")
            for i, course in enumerate(results, 1):
                print(f"{i}. {course.get('name')}")
                print(f"   ID: {course.get('courseId')}")
                print(f"   Duration: {course.get('duration', 'Not specified')}")
                
                # Extract and display partners
                if "partners" in course and course["partners"]:
                    partners = [p["name"] for p in course["partners"]]
                    print(f"   Provider: {', '.join(partners)}")
                
                # Display rating if available
                if "rating" in course:
                    print(f"   Rating: {course.get('rating')}")
                
                # Display a snippet of the description
                if "description" in course and course["description"]:
                    desc = course["description"]
                    if len(desc) > 100:
                        desc = desc[:97] + "..."
                    print(f"   Description: {desc}")
                print()
        
        elif query_type == "course_info":
            # Handle single course info
            course = data["response"][0]["data"]["Course"]
            
            print(f"Course: {course.get('name')}")
            print(f"Slug: {course.get('slug')}")
            print(f"URL: https://www.coursera.org/learn/{course.get('slug')}")
            
            # Display instructors
            if "instructors" in course and course["instructors"]:
                print("\nInstructors:")
                for instructor in course["instructors"]:
                    print(f"- {instructor.get('fullName')}, {instructor.get('title', '')}")
            
            # Display partners
            if "partners" in course and course["partners"]:
                print("\nPartners:")
                for partner in course["partners"]:
                    print(f"- {partner.get('name')}")
            
            # Display description
            if "description" in course and course["description"]:
                print("\nDescription:")
                print(course["description"])
        
        elif query_type == "specializations":
            # Handle specialization search results
            if "data" in data["response"][0] and "SpecializationResultsV2" in data["response"][0]["data"]:
                results = data["response"][0]["data"]["SpecializationResultsV2"]["elements"]
                total = data["response"][0]["data"]["SpecializationResultsV2"]["total"]
                
                print(f"Found {total} specializations matching your query\n")
                for i, spec in enumerate(results, 1):
                    print(f"{i}. {spec.get('name')}")
                    print(f"   URL: https://www.coursera.org/specializations/{spec.get('slug')}")
                    
                    # Display partners
                    if "partners" in spec and spec["partners"]:
                        partners = [p["name"] for p in spec["partners"]]
                        print(f"   Partners: {', '.join(partners)}")
                    
                    # Display courses count
                    if "courses" in spec:
                        print(f"   Courses: {len(spec['courses'])}")
                    
                    # Display a snippet of the description
                    if "description" in spec and spec["description"]:
                        desc = spec["description"]
                        if len(desc) > 100:
                            desc = desc[:97] + "..."
                        print(f"   Description: {desc}")
                    print()
            else:
                print("No specialization data found in response")
                print("Raw response:")
                print(json.dumps(data["response"], indent=2))
    
    except (KeyError, IndexError, TypeError) as e:
        print(f"Error parsing GraphQL response: {e}")
        print("Raw response:")
        print(json.dumps(data["response"], indent=2))


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
    parser = argparse.ArgumentParser(description="Explore Coursera's GraphQL API")
    parser.add_argument("--query", type=str, default="python programming", 
                       help="Search query (default: 'python programming')")
    parser.add_argument("--course-id", type=str, default="",
                       help="Course ID to retrieve detailed information")
    parser.add_argument("--specializations", action="store_true",
                       help="Search for specializations instead of courses")
    parser.add_argument("--limit", type=int, default=5,
                       help="Maximum number of results to return (default: 5)")
    parser.add_argument("--output", type=str, default="",
                       help="Save results to specified JSON file")
    parser.add_argument("--debug", action="store_true",
                       help="Enable debug mode for verbose output")
    
    args = parser.parse_args()
    client = CourseraGraphQLClient(debug=args.debug)
    results = {}
    
    # Execute queries based on command-line arguments
    if args.course_id:
        # Get details for a specific course
        print(f"Getting GraphQL information for course ID '{args.course_id}'...")
        course_results = client.get_course_info(args.course_id)
        display_results(course_results, "course_info")
        results["course_info"] = course_results
    
    elif args.specializations:
        # Search for specializations
        print(f"Searching Coursera for specializations matching '{args.query}'...")
        spec_results = client.search_specializations(args.query, args.limit)
        display_results(spec_results, "specializations")
        results["specializations"] = spec_results
    
    else:
        # Default: search for courses
        print(f"Searching Coursera for courses matching '{args.query}'...")
        course_results = client.search_courses(args.query, args.limit)
        display_results(course_results, "courses")
        results["courses"] = course_results
    
    # Save results if output file is specified
    if args.output and results:
        save_results(results, args.output)


if __name__ == "__main__":
    main()