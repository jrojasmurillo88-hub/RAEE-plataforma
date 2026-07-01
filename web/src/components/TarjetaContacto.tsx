import type { ContactoFallback } from "@/lib/objetos";

export default function TarjetaContacto({
  etiqueta,
  icono,
  contacto,
}: {
  etiqueta: string;
  icono: string;
  contacto: ContactoFallback;
}) {
  return (
    <div className="rounded-lg border border-amber-200 bg-amber-50 p-4">
      <div className="flex items-center gap-2">
        <span className="text-xl">{icono}</span>
        <span className="font-semibold text-gray-900">{etiqueta}</span>
      </div>
      <p className="mt-2 text-sm text-gray-700">{contacto.mensaje}</p>
      <div className="mt-3 flex flex-col gap-2 text-sm">
        <a
          href={`tel:${contacto.lineaCelular.replace(/\s/g, "")}`}
          className="font-medium text-emerald-700 underline"
        >
          📱 Llama a la línea {contacto.lineaCelular}
        </a>
        <a
          href={`tel:${contacto.lineaFija.replace(/[^\d+]/g, "")}`}
          className="font-medium text-emerald-700 underline"
        >
          ☎️ O al teléfono fijo {contacto.lineaFija}
        </a>
        {contacto.linkUrl && (
          <a
            href={contacto.linkUrl}
            target="_blank"
            rel="noopener noreferrer"
            className="mt-1 inline-block w-full rounded-lg bg-emerald-600 px-3 py-2 text-center text-sm font-semibold text-white hover:bg-emerald-700"
          >
            🌐 {contacto.linkLabel ?? contacto.linkUrl}
          </a>
        )}
      </div>
    </div>
  );
}
