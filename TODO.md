# Roadmap

## Potential issues

- Security verification in macOS
- automatic driver installation that is platform-agnostic (make file?)

## Known issues

- [ ] Logger does not work in stdout and filestream yet

## Short-term roadmap

- [ ] Create `default_config.yml`, with `config.yml` overriding default options
- [ ] Decouple queries from config
- [x] Move config out of the imdb library, consider renaming to `imdb_config`
- [ ] Verify that a season is aired before obtaining ratings
- [ ] Implement plotting with Matplotlib
  - [ ] Mark each season beginning on plot
- [ ] Store scraped data via MongoDb
- [ ] Scrape all TV series with chron
- [ ] _Nice to have:_ Provide (optionally configured) key statistics
  - [ ] Average rating for each season
  - [ ] Number of raters for each episode

Note: for now, we maintain local SeriesRatings objects for compatibility purposes (in case we want to store local objects only, and forego DBs). In the future, we expect to use DBs only. Transactions with the DB should be _stateless_. 

## Medium-term roadmap

- [ ] Package as a pip-package
- [ ] More extensive CLI commands
- [ ] Admin panel hosted by flask
