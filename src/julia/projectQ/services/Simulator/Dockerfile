FROM julia:1.1.0-stretch
LABEL maintainer = "Jan Piotraschke"

# working wir in the image
WORKDIR /projectQ/

# install required packages
ADD Project.toml ./
ADD Manifest.toml ./
RUN julia --project=@. -e "import Pkg; Pkg.instantiate()"
# procompile packages, so they already are, when julia is executed
RUN julia --project=@. -e "import Pkg; Pkg.API.precompile()"

# entrypoint will serve as the base for the command specified in the docker-compose.yml
# `--project=@.` is needed to have access to the packages installed above when running your code
ENTRYPOINT ["julia", "--project=@."]

