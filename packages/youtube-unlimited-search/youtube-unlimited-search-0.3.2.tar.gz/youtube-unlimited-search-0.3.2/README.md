# Youtube Unlimited Search
Allow you to search in youtube without care about requests limitation
## Example

you can use the search tool as following:

```pip install youtube-unlimited-search```

```python
from youtube_unlimited_search import YoutubeUnlimitedSearch

results = YoutubeUnlimitedSearch('search terms', max_results=10).get()

print(results)
# returns a dictionary