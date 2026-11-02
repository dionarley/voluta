{ pkgs ? import <nixpkgs> { } }:
let
  # Bibliotecas de sistema usadas pelo Qt/PySide6 no Linux.
  # O wheel do PySide6 não inclui libGL, xcb, X11 etc.
  qtRuntimeLibs = with pkgs; [
    libglvnd
    libxkbcommon
    libxcb
    libxcb-util
    libxcb-image
    libxcb-keysyms
    libxcb-render-util
    libxcb-wm
    libxcb-cursor
    libX11
    libXext
    libXrender
    libXi
    libSM
    libICE
    libXcursor
    libXrandr
    libXfixes
    libXcomposite
    libXdamage
    libXtst
    dbus
    libdrm
    krb5
    openssl
    zstd
    brotli
    fontconfig
    freetype
    zlib
  ];
in
pkgs.mkShell {
  packages = [ pkgs.uv ];

  # Permite que o PySide6 encontre as bibliotecas compartilhadas no NixOS.
  LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath qtRuntimeLibs;
}
