{ lib
, pkgs
, python3
}:
python3.pkgs.buildPythonPackage rec {
  pname = "kebihelp";
  version = "0.1.2";
  pyproject = true;

  src = ./.;

  nativeBuildInputs = [
    python3.pkgs.setuptools
    python3.pkgs.wheel
    pkgs.qt5.wrapQtAppsHook
  ];

  buildInputs = [
    pkgs.qt5.qtbase
    pkgs.qt5.qtwayland
    pkgs.qt5.qttools
    pkgs.qt5.qtdeclarative
  ];


  propagatedBuildInputs = [
    python3.pkgs.prettytable
    python3.pkgs.pyqt5
    python3.pkgs.pyqt5-sip
  ];

  pythonImportsCheck = [ "kebihelp" ];

  postInstall = ''
    wrapProgram $out/bin/kebihelp \
      --prefix PYTHONPATH : $out/lib/python3.11/site-packages:${pkgs.python311Packages.prettytable}/lib/python3.11/site-packages:${pkgs.python311Packages.pyqt5}/lib/python3.11/site-packages:${pkgs.python311Packages.pyqt5_sip}/lib/python3.11/site-packages:${pkgs.python311Packages.wcwidth}/lib/python3.11/site-packages
  '';

  meta = with lib; {
    description = "A universal Keybinding helper written in Python and QT5";
    homepage = "https://github.com/juienpro/kebihelp";
    changelog = "https://github.com/juienpro/kebihelp/blob/${src.rev}/CHANGELOG.md";
    license = licenses.mit;
    # maintainers = with maintainers; [ ];
    mainProgram = "kebihelp";
  };
}
