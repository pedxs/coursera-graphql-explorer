#!/usr/bin/env python3
"""
Coursera GraphQL API - Final Implementation

This script implements the exact query structure from the Coursera GraphQL API
with proper handling of results.
"""

import requests
import json
import argparse
from typing import Dict, List, Any, Optional


class CourseraGraphQLClient:
    """Client for interacting with Coursera's GraphQL API using actual query structure"""
    
    def __init__(self, debug: bool = False):
        """
        Initialize the GraphQL client
        
        Args:
            debug: Enable debug mode for verbose logging
        """
        self.base_url = "https://www.coursera.org"
        self.graphql_endpoint = f"{self.base_url}/graphql-gateway"
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
        params = {
            "opname": operation_name
        }
        
        payload = {
            "operationName": operation_name,
            "variables": variables,
            "query": query
        }
        
        if self.debug:
            print(f"GraphQL Request to {self.graphql_endpoint}:")
            print(f"Operation: {operation_name}")
            print(f"Variables: {json.dumps(variables, indent=2)}")
        
        response = requests.post(
            self.graphql_endpoint, 
            headers=self.headers, 
            params=params,
            json=payload
        )
        
        if self.debug:
            print(f"Response Status: {response.status_code}")
        
        return {
            "status_code": response.status_code,
            "response": response.json() if response.status_code == 200 else response.text
        }
    
    def search(self, query: str, limit: int = 10) -> Dict[str, Any]:
        """
        Search using Coursera's actual GraphQL query structure
        
        Args:
            query: Search term
            limit: Maximum number of results to return
            
        Returns:
            Dict containing search results or error information
        """
        operation_name = "Search"
        graphql_query = """query Search($requests: [Search_Request!]!) {
  SearchResult {
    search(requests: $requests) {
      ...SearchResult
      __typename
    }
    __typename
  }
}

fragment SearchResult on Search_Result {
  elements {
    ...SearchHit
    __typename
  }
  facets {
    ...SearchFacets
    __typename
  }
  pagination {
    cursor
    totalElements
    __typename
  }
  totalPages
  source {
    indexName
    recommender {
      context
      hash
      __typename
    }
    __typename
  }
  __typename
}

fragment SearchHit on Search_Hit {
  ...SearchArticleHit
  ...SearchProductHit
  ...SearchSuggestionHit
  __typename
}

fragment SearchArticleHit on Search_ArticleHit {
  aeName
  careerField
  category
  createdByName
  firstPublishedAt
  id
  internalContentEpic
  internalProductLine
  internalTargetKw
  introduction
  islocalized
  lastPublishedAt
  localizedCountryCd
  localizedLanguageCd
  name
  subcategory
  topics
  url
  skill: skills
  __typename
}

fragment SearchProductHit on Search_ProductHit {
  avgProductRating
  cobrandingEnabled
  completions
  duration
  id
  imageUrl
  isCourseFree
  isCreditEligible
  isNewContent
  isPartOfCourseraPlus
  name
  numProductRatings
  parentCourseName
  parentLessonName
  partnerLogos
  partners
  productCard {
    ...SearchProductCard
    __typename
  }
  productDifficultyLevel
  productDuration
  productType
  skills
  url
  videosInLesson
  translatedName
  translatedSkills
  translatedParentCourseName
  translatedParentLessonName
  tagline
  __typename
}

fragment SearchSuggestionHit on Search_SuggestionHit {
  id
  name
  score
  __typename
}

fragment SearchProductCard on ProductCard_ProductCard {
  id
  canonicalType
  marketingProductType
  productTypeAttributes {
    ... on ProductCard_Specialization {
      ...SearchProductCardSpecialization
      __typename
    }
    ... on ProductCard_Course {
      ...SearchProductCardCourse
      __typename
    }
    ... on ProductCard_Clip {
      ...SearchProductCardClip
      __typename
    }
    ... on ProductCard_Degree {
      ...SearchProductCardDegree
      __typename
    }
    __typename
  }
  __typename
}

fragment SearchProductCardSpecialization on ProductCard_Specialization {
  isPathwayContent
  __typename
}

fragment SearchProductCardCourse on ProductCard_Course {
  isPathwayContent
  rating
  reviewCount
  __typename
}

fragment SearchProductCardClip on ProductCard_Clip {
  canonical {
    id
    __typename
  }
  __typename
}

fragment SearchProductCardDegree on ProductCard_Degree {
  canonical {
    id
    __typename
  }
  __typename
}

fragment SearchFacets on Search_Facet {
  name
  nameDisplay
  valuesAndCounts {
    ...ValuesAndCounts
    __typename
  }
  __typename
}

fragment ValuesAndCounts on Search_FacetValueAndCount {
  count
  value
  valueDisplay
  __typename
}"""
        
        variables = {
            "requests": [
                {
                    "entityType": "PRODUCTS",
                    "limit": limit,
                    "disableRecommender": True,
                    "maxValuesPerFacet": 1000,
                    "facetFilters": [],
                    "cursor": "0",
                    "query": query
                },
                {
                    "entityType": "SUGGESTIONS",
                    "limit": 7,
                    "disableRecommender": True,
                    "maxValuesPerFacet": 1000,
                    "facetFilters": [],
                    "cursor": "0",
                    "query": query
                }
            ]
        }
        
        return self.execute_query(operation_name, graphql_query, variables)


def display_results(data: Dict[str, Any]) -> None:
    """
    Pretty print GraphQL query results
    
    Args:
        data: API response data
    """
    print("\n===== SEARCH RESULTS =====\n")
    
    if data["status_code"] != 200:
        print(f"GraphQL request failed with status code: {data['status_code']}")
        print(f"Error: {data['response']}")
        return
    
    try:
        search_results = data["response"]["data"]["SearchResult"]["search"]
        
        # Display product results
        product_results = next((r for r in search_results if r["source"]["indexName"] == "prod_all_launched_products_term_optimization"), None)
        
        if product_results and product_results["elements"]:
            total = product_results["pagination"]["totalElements"]
            print(f"Found {total} products matching your query\n")
            
            for i, hit in enumerate(product_results["elements"], 1):
                if hit["__typename"] == "Search_ProductHit":
                    print(f"{i}. {hit.get('name')}")
                    print(f"   Type: {hit.get('productType')}")
                    print(f"   URL: {hit.get('url')}")
                    
                    if hit.get("isCourseFree"):
                        print("   FREE COURSE")
                    
                    if hit.get("isPartOfCourseraPlus"):
                        print("   Included in Coursera Plus")
                    
                    if hit.get("avgProductRating"):
                        print(f"   Rating: {hit.get('avgProductRating')} ({hit.get('numProductRatings')} reviews)")
                    
                    if hit.get("partners"):
                        print(f"   Partners: {', '.join(hit.get('partners'))}")
                    
                    if hit.get('skills'):
                        print(f"   Skills: {', '.join(hit.get('skills')[:3])}")
                        if len(hit.get('skills', [])) > 3:
                            print(f"           + {len(hit.get('skills')) - 3} more")
                    
                    if hit.get('tagline'):
                        print(f"   Tagline: {hit.get('tagline')}")
                    
                    print()
        else:
            print("No product results found.")
        
        # Display suggestion results
        suggestion_results = next((r for r in search_results if r["source"]["indexName"] == "test_suggestions"), None)
        
        if suggestion_results and suggestion_results["elements"]:
            print("\n===== SEARCH SUGGESTIONS =====\n")
            for i, hit in enumerate(suggestion_results["elements"], 1):
                if hit["__typename"] == "Search_SuggestionHit":
                    print(f"{i}. {hit.get('name')}")
        
        # Display facets if available
        if product_results and product_results.get("facets"):
            facets_with_values = [f for f in product_results["facets"] if f["valuesAndCounts"]]
            if facets_with_values:
                print("\n===== AVAILABLE FILTERS =====\n")
                for facet in facets_with_values:
                    print(f"{facet['nameDisplay']}:")
                    for val in facet["valuesAndCounts"][:5]:  # Show top 5 values
                        print(f"  - {val['valueDisplay']} ({val['count']})")
                    
                    if len(facet["valuesAndCounts"]) > 5:
                        print(f"  + {len(facet['valuesAndCounts']) - 5} more options")
                    print()
    
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


def extract_course_info(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Extract structured course information from the response
    
    Args:
        data: API response data
        
    Returns:
        List of course information dictionaries
    """
    courses = []
    
    if data["status_code"] != 200:
        return courses
    
    try:
        search_results = data["response"]["data"]["SearchResult"]["search"]
        product_results = next((r for r in search_results if r["source"]["indexName"] == "prod_all_launched_products_term_optimization"), None)
        
        if product_results and product_results["elements"]:
            for hit in product_results["elements"]:
                if hit["__typename"] == "Search_ProductHit":
                    course = {
                        "id": hit.get("id"),
                        "name": hit.get("name"),
                        "type": hit.get("productType"),
                        "url": hit.get("url"),
                        "is_free": hit.get("isCourseFree", False),
                        "is_coursera_plus": hit.get("isPartOfCourseraPlus", False),
                        "rating": hit.get("avgProductRating"),
                        "review_count": hit.get("numProductRatings"),
                        "partners": hit.get("partners", []),
                        "skills": hit.get("skills", []),
                        "tagline": hit.get("tagline")
                    }
                    courses.append(course)
    except (KeyError, IndexError, TypeError):
        pass
    
    return courses


def main() -> None:
    """Main entry point for the script"""
    parser = argparse.ArgumentParser(description="Search Coursera using their GraphQL API")
    parser.add_argument("--query", type=str, default="python", 
                       help="Search query (default: 'python')")
    parser.add_argument("--limit", type=int, default=10,
                       help="Maximum number of results to return (default: 10)")
    parser.add_argument("--output", type=str, default="",
                       help="Save results to specified JSON file")
    parser.add_argument("--debug", action="store_true",
                       help="Enable debug mode for verbose output")
    parser.add_argument("--extract", action="store_true",
                       help="Extract structured course information only")
    
    args = parser.parse_args()
    client = CourseraGraphQLClient(debug=args.debug)
    
    # Execute the search query
    print(f"Searching Coursera for '{args.query}'...")
    results = client.search(args.query, args.limit)
    
    # Display and optionally save results
    if args.extract:
        courses = extract_course_info(results)
        print(f"Found {len(courses)} courses")
        if courses:
            print(json.dumps(courses, indent=2))
    else:
        display_results(results)
    
    if args.output:
        save_results(results, args.output)


if __name__ == "__main__":
    main()