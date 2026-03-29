    {
      description = "Python 3.13 development environment";
      outputs = { self, nixpkgs }:
      let
        system = "x86_64-linux";
        pkgs = import nixpkgs {
          inherit system;
          config.allowUnfree = true;
        };
      in {
        devShells.${system}.default = pkgs.mkShell {
          buildInputs = with pkgs; [
            python313
            python313Packages.spacy
            python313Packages.pyinstaller
          ];
        };
      };
    }
