{ buildPythonPackage, fastbencode, schema }:
let
  # Share with setup.py
  verinfo = builtins.fromJSON (builtins.readFile ./version.json);
in
buildPythonPackage {
  inherit (verinfo) pname version;
  src = ./.;
  propagatedBuildInputs = [ fastbencode schema ];
}
