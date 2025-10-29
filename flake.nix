{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };
        pythonEnv = pkgs.python3.withPackages (ps: with ps; [
          pdf2image
          pytesseract
          opencv4
          numpy
          matplotlib
        ]);
      in {
        devShells.default = pkgs.mkShell {
          buildInputs = with pkgs; [
          ];
          shellHook = ''
            export PATH="${pythonEnv}/bin:$PATH"
            export PATH="${self.outPath}/bin:$PATH"
          '';
        };
      });
}
