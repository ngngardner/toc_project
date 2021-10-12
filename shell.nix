<<<<<<< HEAD
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
=======
(import
  (
    let
      lock = builtins.fromJSON (builtins.readFile ./flake.lock);
    in
    fetchTarball {
      url = "https://github.com/edolstra/flake-compat/archive/${lock.nodes.flake-compat.locked.rev}.tar.gz";
      sha256 = lock.nodes.flake-compat.locked.narHash;
    }
  )
  {
    src = ./.;
  }).shellNix
  
>>>>>>> 837e032a82422226af5209cc4e15e7fb8dc0ab89
