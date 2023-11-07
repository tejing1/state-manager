{
  inputs.nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";

  outputs = { self, nixpkgs }@inputs: {
    packagesFunc = pkgs: let
      python = pkgs.python3;
      inherit (python.pkgs) toPythonApplication callPackage;
    in {
      state-manager = toPythonApplication (callPackage ./src/package.nix {});
    };
    packages = let
      defaultPackage = defaultAttr: packages: packages // { default = packages.${defaultAttr}; };
    in nixpkgs.lib.genAttrs [ "x86_64-linux" "aarch64-linux" ] (system:
      defaultPackage "state-manager" (
        self.packagesFunc nixpkgs.legacyPackages.${system}
      )
    );
  };
}
