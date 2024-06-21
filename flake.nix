{
  description = "kebihelp flake";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
  };

  outputs = { self, nixpkgs }:
    let
      supportedSystems = [ "x86_64-linux" "aarch64-linux" "x86_64-darwin" "aarch64-darwin" ];
      forAllSystems = nixpkgs.lib.genAttrs supportedSystems;
      pkgsFor = nixpkgs.legacyPackages;
    in
    {
      packages = forAllSystems (system: {
        default = self.packages.${system}.kebihelp;
        kebihelp = pkgsFor.${system}.callPackage ./default.nix { };
      });

      defaultPackage = forAllSystems (system: self.packages.${system}.default);
    };
}
