FROM julia:1.1.0-stretch
LABEL maintainer = "Jan Piotraschke"

# working wir in the image
WORKDIR /projectQ/

# locally installing packages and their dependencies by puttinng the packages into development mode
# 'using' statement for precompilation (though it does not work correctly, the precompilation is triggered again, when the container is started)
COPY ./ ./
RUN julia -e 'using Pkg; Pkg.develop( PackageSpec( path="/projectQ/packages/EventSystem/" ) ); using EventSystem'
RUN julia -e 'using Pkg; Pkg.develop( PackageSpec( path="/projectQ/packages/Simulation/" ) );  using Simulation'
RUN julia -e 'using Pkg; Pkg.develop( PackageSpec( path="/projectQ/services/Simulator/" ) );   using Simulator'

ENTRYPOINT ["julia"]

