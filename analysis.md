# Coursera GraphQL API Analysis

## Exploration Results

We've attempted to explore Coursera's GraphQL API by sending various test queries to the endpoint:
```
https://www.coursera.org/graphql-gateway?opname=Search
```

Our exploration revealed several key points:

1. **Introspection Disabled**: The API has introspection disabled (common in production APIs for security), making it harder to discover the schema:
   ```
   "GraphQL introspection is not allowed by Apollo Server, but the query contained __schema or __type"
   ```

2. **Type System Clues**: From error messages, we know the API has these types:
   - `Search_Request`
   - `Search_ProductHit`
   - `Search_Result`
   - `Search_Facet`
   - `Search_Context`
   - `Search_Error`

3. **Field Structure**: Error messages show:
   - The `Search_ProductHit` type has `id` and `name` fields but not `slug`
   - A field called `partners` is a list of strings `[String!]`, not an object with subfields
   - The API has a `CitySearch` field but it doesn't accept `query` or `limit` arguments

4. **Query Root Issues**: We couldn't find the correct entry point:
   - Tried `search`, `searchV3`, but got errors
   - May need the exact field name used on the Coursera website

## Next Steps

To properly work with this API, we should:

1. Use browser network tools to capture actual GraphQL requests when searching on Coursera's website
2. Examine working queries to understand:
   - The correct operation name
   - Required headers (cookies, tokens, etc.)
   - Valid field patterns and arguments
   - Correct type names and structure

3. Create proper test cases based on actual working queries

## Working with Protected APIs

This is a common pattern with commercial APIs that aren't publicly documented. To work with them:

1. Always respect the terms of service and rate limits
2. Consider legal implications before scraping or extensive API use
3. Look for official APIs as an alternative (Coursera might have a partner API program)
4. Structure requests exactly as the web application does
5. Be prepared for API changes that could break your integration