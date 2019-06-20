# API

## TVSeries

### uri: POST /tv-series

**Sample POST request body**

```json
{
  "name": "How to Sell Drugs Online (Fast)",
  "series_rating": 8.1, 
  "episode_ratings": [
    {
      "season": 1, 
      "ratings": [
        {
          "episode_number": 1,
          "rating": 8.2
        }, 
        {
          "episode_number": 2,
          "rating": 8.4
        },
        {
          "episode_number": 3,
          "rating": 8.3
        },
        {
          "episode_number": 4,
          "rating": 8.4
        },
        {
          "episode_number": 5,
          "rating": 8.4
        },
        {
          "episode_number": 6,
          "rating": 8.9
        }
      ]
    }
  ]
}
```