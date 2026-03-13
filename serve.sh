#!/bin/bash
# Local Jekyll server using Docker
# Access at http://localhost:4000

cd "$(dirname "$0")"

docker run --rm -it \
  -v "$PWD":/srv/jekyll \
  -p 4000:4000 \
  -e JEKYLL_ENV=development \
  jekyll/jekyll:4 \
  bash -c "gem install webrick && bundle install && jekyll serve --host 0.0.0.0 --future --livereload"
