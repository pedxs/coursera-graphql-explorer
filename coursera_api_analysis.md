# Coursera GraphQL API Analysis

## Overview
This document contains an analysis of Coursera's GraphQL API and how to effectively interact with it.

## API Endpoint
```
https://www.coursera.org/graphql-gateway?opname={operationName}
```

## Authentication
The API appears to allow anonymous access for basic searches, but likely requires authentication for personalized features or course enrollment.

## API Structure

### GraphQL Query Structure
The GraphQL API uses the following overall query structure:

```graphql
query Search($requests: [Search_Request!]!) {
  SearchResult {
    search(requests: $requests) {
      ...SearchResult
      __typename
    }
    __typename
  }
}
```

### Key Types
The API uses several key GraphQL types:

1. `Search_Request` - The input type for search requests
2. `Search_Result` - The result type for search operations
3. `Search_ProductHit` - Represents a course, specialization, or other product
4. `Search_SuggestionHit` - Represents a search suggestion
5. `Search_ArticleHit` - Represents an article or blog post
6. `Search_Facet` - Represents a search filter category

### Query Variables
Requests require a structured variables object:

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

### Multiple Request Types
The API allows multiple request types in a single query:

1. `PRODUCTS` - Search for courses, specializations, etc.
2. `SUGGESTIONS` - Get search suggestions based on the query

### Response Structure
The response structure contains:

1. Search results in `data.SearchResult.search` (array of search result objects)
2. Each search result contains:
   - `elements` - The actual search results
   - `facets` - Available filters
   - `pagination` - Cursor-based pagination info
   - `source` - Information about the search index used

### Product Fields
Products contain many fields, including:

- `id` - Unique identifier
- `name` - Product name
- `productType` - Type (COURSE, SPECIALIZATION, etc.)
- `isCourseFree` - Whether the course is free
- `isPartOfCourseraPlus` - Whether it's included in Coursera Plus
- `skills` - Array of skills taught
- `partners` - Array of partner institutions/companies
- `avgProductRating` - Average rating
- `numProductRatings` - Number of ratings
- `url` - URL path to the product

## Tips for Integration

1. **Exact Query Structure**: Follow the exact query structure with all fragments
2. **Request Batching**: Use the ability to batch multiple entity types in a single request
3. **Pagination**: Implement cursor-based pagination for more results
4. **Facet Filtering**: Use the facetFilters array to filter results
5. **Error Handling**: Handle GraphQL errors properly, as the API can return both HTTP and GraphQL errors

## Challenges and Limitations

1. **No Introspection**: The API doesn't support GraphQL introspection, making schema discovery difficult
2. **Rate Limiting**: There appears to be rate limiting or IP-based restrictions for anonymous requests. Some queries that should return results may return empty data sets, particularly after multiple requests.
3. **Schema Changes**: The API schema may change without notice
4. **Field Selection**: All relevant fragments must be included, or the query will fail
5. **Geolocation Restrictions**: The API may return different results based on the user's location
6. **Authentication Requirements**: Some queries may only return full results when authenticated
7. **Different Search Indices**: The API uses different search indices (`prod_all_launched_products_term_optimization` vs. `test_suggestions`) which may have different behaviors

## Tools for Testing

1. Browser Network Inspector to capture live requests
2. Our custom Python client for experimentation
3. GraphQL query variables for modifying search parameters

## Conclusion
The Coursera GraphQL API is a powerful but complex interface that requires careful query construction. By following the exact query structure and understanding the response format, we can effectively integrate with this API for course discovery and search functionality.