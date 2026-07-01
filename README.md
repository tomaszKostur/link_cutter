Link cutter PoC
===============

What wasn't entirely clear from the requirements was the expected API input/output design.
I implemented it in what I consider the most standard way.

Create short url
================

The API exposes a POST endpoint at linkmap/ that accepts a request body in the following format:

{
  "orig_url": "<THE URL AS A STRING>"
}

The response contains the generated short URL:

{
  "short_url": "<THE SHORT URL AS A STRING>"
}

Accessing the returned short URL redirects the client to the original URL provided in the request.

Reverse search
==============

To retrieve the original URL, I implemented a GET endpoint at:
linkmap/<url_hash>
The url_hash is the 8-digit hash contained in the short URL returned by the POST /linkmap/ request.

I may agree that requiring knowledge of which part of the short url represents hash, may not the most convenient, yet I believe path parameter is standard way to get details about some single elements of bysiness entity models.
The other approach might be expose another GET request parametrised with full-length "short_url" in request body.

Notes
=====

There is some possibility of collision while creating hew short url, due to truncated hash. This limitation migt be considered to fix in future and S suffecient for version 0.1.

The linkmap_all/ path is considered primarily for debugging. It's provided almost out of the box by the framework. Not required so no test written for the path.

Before merging into production, I would also clean up the migration history and leave only a single initial migration.