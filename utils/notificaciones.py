from flask import current_app, render_template_string
from flask_mail import Message
from app_extensions import mail
from datetime import datetime


def _destinatario():
    return current_app.config.get('MAIL_DESTINATARIO')


def enviar_resumen_venta(venta):
    """Envía resumen de venta al administrador."""
    try:
        detalles = "\n".join([
            f"  - {d.producto.nombre} x{d.cantidad} = S/ {d.subtotal:.2f}"
            for d in venta.detalles.all()
        ])

        cuerpo = f"""
Almacén Anita New Style — Nueva Venta Registrada
═══════════════════════════════════════════════

N° Venta:      {venta.numero_venta}
Fecha:         {venta.fecha.strftime('%d/%m/%Y %H:%M')}
Método de pago:{venta.metodo_pago_label}
Cliente:       {venta.cliente_nombre or 'Sin nombre'}

Productos:
{detalles}

─────────────────────────────────────
Subtotal:  S/ {float(venta.subtotal):.2f}
Descuento: S/ {float(venta.descuento):.2f}
TOTAL:     S/ {float(venta.total):.2f}
═══════════════════════════════════════════════
        """

        msg = Message(
            subject=f'[Venta] {venta.numero_venta} — S/ {venta.total:.2f}',
            sender=current_app.config['MAIL_USERNAME'],
            recipients=[_destinatario()],
            body=cuerpo
        )
        mail.send(msg)
    except Exception as e:
        current_app.logger.error(f'Error enviando correo de venta: {e}')


def enviar_alerta_stock(productos_bajos):
    """Envía alerta cuando hay productos con stock bajo."""
    if not productos_bajos:
        return
    try:
        lineas = "\n".join([
            f"  - {p.nombre} → Stock actual: {p.stock} (mínimo: {p.stock_minimo})"
            for p in productos_bajos
        ])

        cuerpo = f"""
Almacén Anita New Style — ⚠️ Alerta de Stock Bajo
═══════════════════════════════════════════════

Los siguientes productos están por debajo del stock mínimo:

{lineas}

Por favor reabastece estos productos a la brevedad.

Fecha: {datetime.utcnow().strftime('%d/%m/%Y %H:%M')}
═══════════════════════════════════════════════
        """

        msg = Message(
            subject=f'⚠️ Alerta: {len(productos_bajos)} producto(s) con stock bajo',
            sender=current_app.config['MAIL_USERNAME'],
            recipients=[_destinatario()],
            body=cuerpo
        )
        mail.send(msg)
    except Exception as e:
        current_app.logger.error(f'Error enviando alerta de stock: {e}')


def enviar_resumen_diario(ventas_hoy, total_hoy, productos_bajos):
    """Envía resumen del día al administrador."""
    try:
        hoy = datetime.utcnow().strftime('%d/%m/%Y')

        # Ventas
        if ventas_hoy:
            lineas_ventas = "\n".join([
                f"  {'✅'} {v.numero_venta:<20} {v.metodo_pago_label:<15} S/ {float(v.total):>8.2f}  —  {v.cliente_nombre or 'Sin nombre'}"
                for v in ventas_hoy
            ])
        else:
            lineas_ventas = "  Sin ventas registradas hoy."

        # Stock bajo
        if productos_bajos:
            lineas_stock = "\n".join([
                f"  {'🔴' if p.sin_stock else '⚠️ '} {p.nombre:<30} Stock: {p.stock:>3}  /  Mínimo: {p.stock_minimo}"
                for p in productos_bajos
            ])
        else:
            lineas_stock = "  ✅ Todo el inventario está en orden."

        # Método de pago más usado
        if ventas_hoy:
            from collections import Counter
            metodos = Counter(v.metodo_pago_label for v in ventas_hoy)
            metodo_top = metodos.most_common(1)[0]
            resumen_metodos = "\n".join([
                f"  • {metodo:<20} {cant} venta{'s' if cant > 1 else ''}"
                for metodo, cant in metodos.items()
            ])
        else:
            resumen_metodos = "  Sin datos."

        cuerpo = f"""
╔══════════════════════════════════════════════════════════════╗
       🏪  ALMACÉN ANITA NEW STYLE — RESUMEN DEL DÍA
╚══════════════════════════════════════════════════════════════╝
  📅 Fecha: {hoy}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  💰 RESUMEN DE VENTAS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{lineas_ventas}

  ┌─────────────────────────────────┐
  │  Total recaudado:  S/ {float(total_hoy):>8.2f}  │
  │  N° de ventas:     {len(ventas_hoy):>3} venta{'s' if len(ventas_hoy) != 1 else ''}      │
  └─────────────────────────────────┘

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  💳 MÉTODOS DE PAGO UTILIZADOS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{resumen_metodos}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  📦 PRODUCTOS CON STOCK BAJO O SIN STOCK
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{lineas_stock}

══════════════════════════════════════════════════════════════
  Correo generado automáticamente por el sistema.
  Almacén Anita New Style — {hoy}
══════════════════════════════════════════════════════════════
        """

        msg = Message(
            subject=f'📊 Resumen del día {hoy} — S/ {float(total_hoy):.2f} — {len(ventas_hoy)} venta{"s" if len(ventas_hoy) != 1 else ""}',
            sender=current_app.config['MAIL_USERNAME'],
            recipients=[_destinatario()],
            body=cuerpo
        )
        mail.send(msg)
    except Exception as e:
        current_app.logger.error(f'Error enviando resumen diario: {e}')