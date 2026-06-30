# MSIG website — Ruby dependencies.
#
# GitHub Pages builds this site natively from these gems; you do NOT need a
# GitHub Action. To preview locally (optional): install Ruby, then run
#   bundle install
#   bundle exec jekyll serve
# and open http://localhost:4000.

source "https://rubygems.org"

# The github-pages gem pins Jekyll and every allowed plugin to exactly the
# versions GitHub Pages runs, so "works locally" == "works when deployed".
gem "github-pages", group: :jekyll_plugins

# Plugins used by the site (also bundled in github-pages, listed for clarity).
group :jekyll_plugins do
  gem "jekyll-seo-tag"
  gem "jekyll-sitemap"
  gem "jekyll-feed"
end

# Timezone database for Windows / JRuby (those platforms don't ship one).
platforms :windows, :jruby do
  gem "tzinfo", ">= 1", "< 3"
  gem "tzinfo-data"
end

# webrick is no longer bundled with Ruby 3+, but `jekyll serve` needs it.
gem "webrick", "~> 1.8"

# NOTE: `wdm` (a native Windows file-watcher) is intentionally NOT included —
# its old release fails to compile on Ruby 3.x. Jekyll's `--watch` falls back to
# polling on Windows, which is perfectly fine for a site this size.
