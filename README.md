# Coursera GraphQL API Explorer

[![GitHub Repository](https://img.shields.io/badge/GitHub-Repository-blue)](https://github.com/pedxs/coursera-graphql-explorer)

## Overview
This project explores and documents Coursera's GraphQL API gateway used for searching courses and other content.

## API Endpoint
```
POST https://www.coursera.org/graphql-gateway?opname=Search
```

## Key Findings

### Restrictions
- GraphQL introspection is disabled (common security practice)
- The endpoint requires specific query structures
- Working with this API requires reverse engineering

### Known Schema Information
Based on our exploration and error messages:

1. The API has types like `Search_Request`, `Search_ProductHit`, `Search_Result`, `Search_Facet`, `Search_Context`, and `Search_Error`
2. The API has fields like `CitySearch` but not `CatalogSearch`
3. The `Search_ProductHit` type has fields for `id` and `name` but not `slug`
4. The query root doesn't have a field called `searchV3` or `search`
5. The `CitySearch` field doesn't accept `query` or `limit` arguments

### Request Format
Requests should be formatted as a JSON array containing a single object with:
- `operationName`: String identifier (e.g., "Search")
- `variables`: Object containing search parameters
- `query`: GraphQL query string

```json
[
  {
    "operationName": "Search",
    "variables": { ... },
    "query": "query Search(...) { ... }"
  }
]
```

### Actual GraphQL Query Structure
We've successfully captured and implemented the exact GraphQL query structure from Coursera's website. See the complete structure in our [coursera_api_analysis.md](./coursera_api_analysis.md) document.

A simplified view:

```graphql
query Search($requests: [Search_Request!]!) {
  SearchResult {
    search(requests: $requests) {
      ...SearchResult
      __typename
    }
  }
}
```

With variables:

```json
"variables": {
  "requests": [
    {
      "entityType": "PRODUCTS",
      "limit": 10,
      "disableRecommender": true,
      "maxValuesPerFacet": 1000,
      "facetFilters": [],
      "cursor": "0",
      "query": "python"
    },
    {
      "entityType": "SUGGESTIONS",
      "limit": 7,
      "disableRecommender": true,
      "maxValuesPerFacet": 1000,
      "facetFilters": [],
      "cursor": "0",
      "query": "python"
    }
  ]
}
```

## Recommendation for Further Work
To effectively use Coursera's GraphQL API, we recommend:

1. **Capture actual browser requests**: Use browser developer tools (Network tab) to capture real GraphQL queries when searching on Coursera's website
2. **Analyze request structure**: Examine the successful queries to understand the correct field names and parameters
3. **Extract query patterns**: Create a library of working query templates for different use cases
4. **Build request generator**: Create helper functions to construct valid GraphQL queries

## Usage

### Interactive Runner
For easy exploration of all examples, use the interactive runner:
```bash
python3 run_examples.py
```

This provides a menu-based interface to run all examples, view documentation, and explore the API capabilities.

### Exploration Script
Run the exploration script to test different query approaches:
```bash
python3 coursera_graphql_test.py
```

This will attempt various queries and log the responses and findings to `coursera_api_findings.md`.

### GraphQL Examples
For examples that demonstrate interacting with Coursera's GraphQL API:

```bash
# Using our reverse-engineered GraphQL query format:
python3 example.py --query "machine learning" --limit 5 --output results.json
```

```bash
# Using the exact GraphQL query structure from Coursera:
python3 coursera_api_final.py --query "machine learning" --limit 10 --output results.json
```

```bash
# Enable debug mode to see request details:
python3 coursera_api_final.py --query "python" --debug
```

```bash
# Extract structured course information in JSON format:
python3 coursera_api_final.py --query "python" --extract
```

These scripts demonstrate:
- Structured GraphQL query building
- Working with GraphQL variables and fragments
- Handling GraphQL response data
- Error handling for GraphQL-specific issues
- Command-line interface for testing GraphQL queries
- Implementation of actual query structure from Coursera's website

## GraphQL API Challenges
Our exploration of Coursera's GraphQL API revealed several challenges:

- **Schema Protection**: GraphQL introspection is disabled, making it difficult to discover the schema
- **Authentication Requirements**: Many queries likely require authentication tokens or specific headers
- **Undocumented Types**: Type names like `CoursesFilters` and `Course` appear to exist but with unclear structures
- **Operation Naming**: The operation name may need to match specific patterns (e.g., `ProductSearch`)
- **Schema Changes**: The API schema may change over time without notice
- **Rate Limiting**: Unauthenticated requests are likely rate-limited

To build a production-ready GraphQL integration with Coursera, you would need to:
1. Capture and analyze actual browser requests
2. Implement proper authentication
3. Keep queries updated as the schema evolves
4. Handle rate limiting and error cases gracefully