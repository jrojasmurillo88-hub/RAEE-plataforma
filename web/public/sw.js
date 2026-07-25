// Service worker mínimo para notificaciones push (check-in 24h post-entrega).
// No cachea nada — su único trabajo es recibir el push y mostrar la notificación.

self.addEventListener("push", (event) => {
  let datos = { titulo: "RAEEconecta", cuerpo: "¿Botaste tu RAEE?", puntoId: null };
  try {
    if (event.data) datos = { ...datos, ...event.data.json() };
  } catch {
    // payload no era JSON, se usa el default
  }

  event.waitUntil(
    self.registration.showNotification(datos.titulo, {
      body: datos.cuerpo,
      icon: "/next.svg",
      badge: "/next.svg",
      data: { puntoId: datos.puntoId, url: "/" },
      tag: "raee-checkin",
    })
  );
});

self.addEventListener("notificationclick", (event) => {
  event.notification.close();
  const url = event.notification.data?.url || "/";
  event.waitUntil(
    self.clients.matchAll({ type: "window", includeUncontrolled: true }).then((clientList) => {
      for (const client of clientList) {
        if ("focus" in client) return client.focus();
      }
      if (self.clients.openWindow) return self.clients.openWindow(url);
    })
  );
});
