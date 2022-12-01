{ pkgs }: {
  deps = [
    pkgs.python38Packages.virtualenv
    pkgs.python38Packages.pip
    pkgs.poetry
    pkgs.nodejs-16_x
    pkgs.python38Full
  ];
  environment.systemPackages = [
    pkgs.ffmpeg
  ];
  env = {
    PYTHON_LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath [
      # Needed for pandas / numpy
      pkgs.stdenv.cc.cc.lib
      pkgs.zlib
      # Needed for pygame
      pkgs.glib
      # Needed for matplotlib
      pkgs.xorg.libX11
    ];
    PYTHONBIN = "${pkgs.python38Full}/bin/python3.8";
    LANG = "en_US.UTF-8";
  };
}