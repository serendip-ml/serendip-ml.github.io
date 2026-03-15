#!/bin/bash
# Local Jekyll server using Docker
# Access at http://localhost:4000

cd "$(dirname "$0")/.." || exit 1

docker run --rm -it \
  -v "$PWD":/site \
  -w /site \
  -p 4000:4000 \
  -p 35729:35729 \
  -e JEKYLL_ENV=development \
  -e BUNDLE_PATH=/site/.vendor/bundle \
  ruby:3.2 \
  bash -c "echo '==> Running bundle install...' && bundle install --jobs=4 && \
           echo '==> Starting Jekyll server...' && bundle exec jekyll serve --host 0.0.0.0 --future --livereload"
