# Virginia Department of Social Services Scraper

Scrapes the Virginia DSS website with the goal of noting any daycares with inspection violations.
I do not live in Virginia, this was a request by another dev.

This is a partial solution, handed off as a proof-of-concept. It currently stops after gathering all the urls that will lead to detailed inspection notes for any daycare with an inspection violation in >=2022. The user only cares about specific violation codes, so their next step will be taking the resulting list of urls and using the existing async methods to request each inspection and parse them for relevent data.

- Uses async requests to gather data in a timely manner.
- Has some retry logic.
- Parses using lxml.
