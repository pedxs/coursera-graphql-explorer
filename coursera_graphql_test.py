import requests
import json

def probe_coursera_graphql():
    """
    Probe Coursera's GraphQL search endpoint with different queries and parameters
    """
    endpoint = "https://www.coursera.org/graphql-gateway?opname=Search"
    
    # Basic headers needed for the request
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    }
    
    # Final attempt with more precise type names based on error messages
    final_attempt_payload = [{
        "operationName": "Search",
        "variables": {
            "requests": [
                {
                    "entityType": "PRODUCTS",
                    "limit": 5,
                    "disableRecommender": True,
                    "query": "python"
                }
            ]
        },
        "query": """
        query Search($requests: [Search_Request!]!) {
          searchV3(requests: $requests) {
            request {
              query
              entityType
            }
            totalCount
            hits {
              __typename
              ... on Search_ProductHit {
                id
                name
                slug
              }
            }
          }
        }
        """
    }]
    
    try:
        # Try final attempt
        print("Testing Coursera GraphQL Search API...")
        final_response = requests.post(endpoint, headers=headers, data=json.dumps(final_attempt_payload))
        print(f"Status Code: {final_response.status_code}")
        
        if final_response.status_code == 200:
            print("Request successful!")
            with open("coursera_search_results.json", "w") as f:
                json.dump(final_response.json(), f, indent=2)
            print("Saved search results to coursera_search_results.json")
            
            # Extract useful information from the response
            results = final_response.json()
            return results
        else:
            print(f"Error: {final_response.text}")
            
            # Document findings in a summary file
            with open("coursera_api_findings.md", "w") as f:
                f.write("# Coursera GraphQL API Exploration Results\n\n")
                f.write("## API Endpoint\n")
                f.write(f"`{endpoint}`\n\n")
                f.write("## Error Details\n")
                f.write("```\n")
                f.write(final_response.text)
                f.write("\n```\n\n")
                f.write("## What We've Learned\n")
                f.write("- Introspection is disabled on this endpoint\n")
                f.write("- The API uses types like `Search_Request`, `Search_ProductHit`, etc.\n")
                f.write("- The query operation might be `searchV3` rather than `search`\n")
                f.write("- To use this API properly, we should capture and analyze actual browser requests\n")
            
            print("Saved findings to coursera_api_findings.md")
            return None
    
    except Exception as e:
        print(f"Error making request: {e}")
        return None

if __name__ == "__main__":
    probe_coursera_graphql()