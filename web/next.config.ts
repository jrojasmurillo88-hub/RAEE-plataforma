import type { NextConfig } from "next";

// react-leaflet inicializa el mapa de forma imperativa y no tolera bien el
// doble montaje de efectos que hace React Strict Mode en desarrollo — eso
// dejaba un marcador "fantasma" superpuesto que bloqueaba los clics reales.
const nextConfig: NextConfig = {
  reactStrictMode: false,
};

export default nextConfig;
