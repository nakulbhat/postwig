{
    description = "Python 3.13 development environment";
    inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    outputs = { self, nixpkgs }:
        let
            system = "x86_64-linux";
            pkgs = import nixpkgs {
                inherit system;
                config.allowUnfree = true;
            };
            en_core_web_sm = pkgs.python313Packages.buildPythonPackage {
                pname = "en_core_web_sm";
                version = "3.8.0";
                src = pkgs.fetchurl {
                    url = "https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.8.0/en_core_web_sm-3.8.0.tar.gz";
                    hash = "sha256-FKLzG8R2r4cBmBnqjJlI+r39RzpELt1rHLpivwwsD1U=";
                };
                pyproject = true;
                build-system = with pkgs.python313Packages; [
                    setuptools
                    wheel
                ];
                dependencies = with pkgs.python313Packages; [
                    spacy
                    rich
                ];
            };
            pythonEnv = pkgs.python313.withPackages (ps: with ps; [
                spacy
                nltk
                en_core_web_sm
            ]);
            postwig = pkgs.writeShellScriptBin "postwig" ''
                exec ${pythonEnv}/bin/python ${./postwig.py} "$@"
            '';
        in {
            packages.${system}.default = postwig;

            apps.${system}.default = {
                type = "app";
                program = "${postwig}/bin/postwig";
            };

            devShells.${system}.default = pkgs.mkShell {
                packages = [ postwig ];
            };
        };
}
