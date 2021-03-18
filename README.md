# scrape-aca-lessons

Scrape lessons information from https://aca.am/

1. First part of homework for first week

Scrape following information for every lesson and collect them in list:

```
[
  {
    "course_name": "Introduction to JavaScript",
    "course_id": "intro-js"
    "course_url": "https://aca.am/en/intro-js.html",
    "price": "76,000 AMD",
    "level": "Beginner",
    "teachers": [{
                   "full_name": "Ruben Karapetyan",
                   "company": "AimHub"
                 },
                 {
                   "full_name": "Angela Hayrapetyan",
                   "company": "SoftConstruct"
                 },
                 {
                   "full_name": "Karen Minasyan",
                   "company": "EPAM Systems"
                 }]
  },
  {...},
  ...
]
```

course_id is last part of course url without .html  <br>

2.Second Part of homework for second week

2.1 Save scraped information in sqllight database. <br>
2.2 write function that checks ever week if there is new lessons or not and send new lessons information to your personal(or test) email.
