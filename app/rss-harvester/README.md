rss-harvester
=============

This is going to be a tool that can harvest css feeds and should be able to do the following things

1.  search the web for rss feeds

2.  classify them into categories

        Country / language
        National, international, world, economical, sport, breaking, weather, culture, science

3.  maybe more to come

This run as instructed only, no automatic searches (yet)

The results should be stored in the main database and should have the following table structure.

        - rssFeeds
                id integer primary key
                rss_name VARCHAR unique
                rss_url  VARCHAR unique
                country_id cross table
                language_id cross table
                category_id cross table