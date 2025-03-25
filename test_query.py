#!/usr/bin/env python3
"""
Test script to fetch from Coursera GraphQL API using the actual query structure
"""

import requests
import json

def main():
    url = 'https://www.coursera.org/graphql-gateway'
    params = {'opname': 'Search'}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'https://www.coursera.org',
        'Referer': 'https://www.coursera.org/search'
    }

    # The exact query structure from your example
    query = """query Search($requests: [Search_Request!]!) {
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

    # The exact variables from your example
    variables = {
        "requests": [
            {
                "entityType": "PRODUCTS",
                "limit": 1,
                "disableRecommender": True,
                "maxValuesPerFacet": 1000,
                "facetFilters": [],
                "cursor": "0",
                "query": "free"
            },
            {
                "entityType": "SUGGESTIONS",
                "limit": 7,
                "disableRecommender": True,
                "maxValuesPerFacet": 1000,
                "facetFilters": [],
                "cursor": "0",
                "query": "free"
            }
        ]
    }

    payload = {
        "operationName": "Search",
        "variables": variables,
        "query": query
    }

    print("Sending request to Coursera GraphQL API...")
    response = requests.post(url, headers=headers, params=params, json=payload)
    print(f"Response status code: {response.status_code}")
    
    # Save the response to file
    with open('coursera_test_response.json', 'w') as f:
        if response.status_code == 200:
            json.dump(response.json(), f, indent=2)
            print("Response saved to coursera_test_response.json")
        else:
            # Save error response
            error_info = {
                "status_code": response.status_code,
                "text": response.text
            }
            json.dump(error_info, f, indent=2)
            print(f"Error response saved to coursera_test_response.json")
            print(f"Error: {response.text}")

if __name__ == "__main__":
    main()