import requests
import json

def search_coursera(query="python", limit=10):
    """
    Perform a search query against Coursera's GraphQL API using observed traffic patterns
    
    Args:
        query: Search term (default: 'python')
        limit: Number of results to return (default: 10)
    
    Returns:
        dict: API response with search results
    """
    endpoint = "https://www.coursera.org/api/autocomplete.v2"
    
    # This is a simpler endpoint that doesn't use GraphQL but works reliably
    params = {
        "q": query,
        "context": "search",
        "limit": str(limit),
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept": "application/json",
        "Referer": "https://www.coursera.org/search",
    }
    
    try:
        response = requests.get(endpoint, params=params, headers=headers)
        print(f"Status code: {response.status_code}")
        
        if response.status_code == 200:
            results = response.json()
            return results
        else:
            print(f"Error: {response.text}")
            return None
    except Exception as e:
        print(f"Exception occurred: {e}")
        return None


def search_graphql(query="python", limit=10):
    """
    Perform a search query against Coursera's GraphQL API
    This is a more accurate representation based on network traffic analysis
    
    Args:
        query: Search term (default: 'python')
        limit: Number of results to return (default: 10)
    
    Returns:
        dict: API response with search results
    """
    endpoint = "https://www.coursera.org/graphqlBatch"
    
    # Headers based on actual browser requests
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept": "*/*",
        "x-csrftoken": "",  # You would need an actual CSRF token
        "X-Requested-With": "XMLHttpRequest",
        "Origin": "https://www.coursera.org",
        "Referer": "https://www.coursera.org/search",
    }
    
    # Corrected GraphQL query based on API error messages
    payload = [
        {
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
        }
    ]
    
    try:
        response = requests.post(endpoint, headers=headers, data=json.dumps(payload))
        print(f"GraphQL Status code: {response.status_code}")
        
        if response.status_code == 200:
            results = response.json()
            return results
        else:
            print(f"GraphQL Error: {response.text}")
            return None
    except Exception as e:
        print(f"GraphQL Exception occurred: {e}")
        return None


def main():
    # Try both methods and save results
    print("\n1. Using the autocomplete API (simpler, more reliable):\n")
    results = search_coursera("python programming")
    
    if results:
        print(f"Found {len(results.get('courses', []))} courses")
        # Save to a file
        with open("coursera_autocomplete_results.json", "w") as f:
            json.dump(results, f, indent=2)
        print("Results saved to coursera_autocomplete_results.json")
        
        # Print first few results
        print("\nSample results:")
        for course in results.get('courses', [])[:3]:
            print(f"- {course.get('name')} ({course.get('domainId')})")
    
    print("\n2. Using the GraphQL API (may require cookies/authentication):\n")
    graphql_results = search_graphql("python programming")
    
    if graphql_results:
        with open("coursera_graphql_working_results.json", "w") as f:
            json.dump(graphql_results, f, indent=2)
        print("GraphQL results saved to coursera_graphql_working_results.json")


if __name__ == "__main__":
    main()