{
  description = "Theory of Computation Project";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/d189bf92f9be23f9b0f6c444f6ae29351bb7125c";
    utils = { url = "github:numtide/flake-utils"; };
    compat = { url = "github:edolstra/flake-compat"; flake = false; };
  };

  outputs = { self, nixpkgs, utils, compat }:
    utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs {
          inherit system;
        };

        python = pkgs.python39;
        projectDir = ./.;
        overrides = pkgs.poetry2nix.overrides.withDefaults (final: prev: {
          # Python dependency overrides go here
        });

        packageName = "traffic_sim";
      in
      {
        packages.${packageName} = pkgs.poetry2nix.mkPoetryApplication {
          inherit python projectDir overrides;
          propogatedBuildInputs = [
            # Non-Python runtime dependencies go here
          ];
        };

        defaultPackage = self.packages.${system}.${packageName};

        devShell = pkgs.mkShell {
          buildInputs = [
            # python
            (pkgs.poetry2nix.mkPoetryEnv {
              inherit python projectDir overrides;
            })
            pkgs.python39Packages.poetry

            # tex
            (pkgs.texlive.combine {
              inherit (pkgs.texlive)
                scheme-small
                xstring
                iftex
                totpages
                environ
                hyperxmp
                ;
            })
          ];
        };
      });
}
