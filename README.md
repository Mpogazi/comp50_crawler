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

- url: https://crawler-concurrency.herokuapp.com/get_companies
method: GET
req_data:
returns: list of all companies in SP 500

- url: https://crawler-concurrency.herokuapp.com/get_company_info
method: POST
req_data: example:
``{
    "name": "Apple Inc."
}``
returns: 
``{
    "name" : "Apple Inc.",
    "symbol": "APPL"
}``

- url: https://crawler-concurrency.herokuapp.com/add_mention
method: POST
req_data: example:
``{
    "name": "Apple Inc.",
    "update": [{"article_title": "Apple is broken", "article_url": "apple.com"}, {"article_title": "Apple is mad","article_url": "lkjdsfasjldkafd.com"}]
}``
returns: ``successfully added mention``

