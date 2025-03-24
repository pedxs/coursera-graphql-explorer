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

### Known Request Variables
Based on our testing and the initial documentation:

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
Run the exploration script:
```bash
python3 coursera_graphql_test.py
```

This will attempt various queries and log the responses and findings to `coursera_api_findings.md`.

## Limitations
Our exploration revealed that this API:
- Has security measures in place to limit programmatic access
- Requires specific types and fields that aren't fully documented
- May need additional headers or authentication for full functionality

To build a production-ready integration, you'll need to monitor for API changes and structure requests exactly according to Coursera's expectations.