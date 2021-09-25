{ pkgs }:
pkgs.mkShell {
  packages = [
    (pkgs.texlive.combine { inherit (pkgs.texlive) 
      scheme-small 
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