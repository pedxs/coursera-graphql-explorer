# Coursera GraphQL API Exploration Results

## API Endpoint
`https://www.coursera.org/graphql-gateway?opname=Search`

## Error Details
```
[{"errors":[{"message":"Cannot query field \"searchV3\" on type \"Query\".","locations":[{"line":3,"column":11}],"extensions":{"code":"GRAPHQL_VALIDATION_FAILED"}},{"message":"Cannot query field \"slug\" on type \"Search_ProductHit\".","locations":[{"line":14,"column":17}],"extensions":{"code":"GRAPHQL_VALIDATION_FAILED"}}]}
]
```

## What We've Learned
- Introspection is disabled on this endpoint
- The API uses types like `Search_Request`, `Search_ProductHit`, etc.
- The query operation might be `searchV3` rather than `search`
- To use this API properly, we should capture and analyze actual browser requests
