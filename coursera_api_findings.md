# Coursera GraphQL API Exploration Results

## API Endpoint
`https://www.coursera.org/graphql-gateway?opname=Search`

## Error Details
```
[{"errors":[{"message":"Unknown type \"CoursesFilters\". Did you mean \"CourseQueries\"?","locations":[{"line":2,"column":84}],"extensions":{"code":"GRAPHQL_VALIDATION_FAILED"}},{"message":"Cannot query field \"CatalogResultsV2\" on type \"Query\".","locations":[{"line":3,"column":11}],"extensions":{"code":"GRAPHQL_VALIDATION_FAILED"}},{"message":"Unknown type \"Course\". Did you mean \"CoursesV1\"?","locations":[{"line":6,"column":22}],"extensions":{"code":"GRAPHQL_VALIDATION_FAILED"}}]}
]
```

## What We've Learned
- Introspection is disabled on this endpoint
- The API uses types like `Search_Request`, `Search_ProductHit`, etc.
- The query operation might be `searchV3` rather than `search`
- To use this API properly, we should capture and analyze actual browser requests
