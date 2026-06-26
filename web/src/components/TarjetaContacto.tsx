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
      <div className="mt-3 flex flex-col gap-1 text-sm">
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
      </div>
    </div>
  );
}
