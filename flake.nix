{
  description = "A very basic flake";

  outputs = { self, nixpkgs }: {
    devShells.x86_64-linux.default =
      let pkgs = nixpkgs.legacyPackages.x86_64-linux;
      in with pkgs;
      mkShell {
        nativeBuildInputs = [ clojure perl python3 racket sqlite ]
          ++ (with ocamlPackages; [ dune_3 findlib ocaml opam ]);
      };
  };
}
