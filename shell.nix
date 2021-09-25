{ pkgs ? import ./nix { } }:
pkgs.mkShell {
  packages = [
    (pkgs.texlive.combine { inherit (pkgs.texlive) 
      scheme-full 
      xstring 
      iftex
      totpages
      environ
      hyperxmp
    ; })

    # nix dev
    pkgs.nixpkgs-fmt
  ];
}