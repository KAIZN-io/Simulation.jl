# Dynamic SDE / ODE Solver

This is the home of our dynamic SDE / ODE solver written in Julia. It is used in Q to run simulations created by the user.

## Usage

To use this package, install it using the Julia package manager.

### Requirements

- Julia v1.0 or higher

## Development

Fire up `julia`, type `]` to get into the package manager, then activate the package with `activate .`. You can now start `using Simulation`.

### Running tests

Yet to be implemented

### Package management

#### Julia
The `Project.toml` and `Manifest.toml` contain the package definitions for Julia. This allwos us to manage packages with Julias built-in package manager. This is how you manage packages with it:

- Open a terminal in the root of the project
- Run `julia`
- type `]` (closing square bracket)
- run `activate .`
- use `add <PackageName>` to add a new package
- use `rm <PackageName>` to remove a package
- use `up <PackageName>` to update a package to a newer version

All your modifications to the packages will be reflected in the `Project.toml` and `Manifest.toml` respectively.

