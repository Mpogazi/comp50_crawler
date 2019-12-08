# comp50_crawler
Final project for the comp 50 class.

## mongo /server usage: 
- url: https://crawler-concurrency.herokuapp.com/add_stock_mentions
method: POST
req_data: example: 
``{
    "name": "Apple Inc.",
    "update": [{"article_title": "Apple is broken", "article_url": "apple.com"}, {"article_title": "Apple is mad","article_url": "lkjdsfasjldkafd.com"}]
}``

- url: https://crawler-concurrency.herokuapp.com/add_user
method: POST
req_data: example: 
``{
    "name": "Fabrice B. Mpogazi",
    "email": "fmpogazi@gmail.com",
    "watchlist": ["Apple Inc.", "Microsoft Inc.", "Google LLC."]
}``

- url: https://crawler-concurrency.herokuapp.com/
method: POST
req_data: example: 
``{}``

