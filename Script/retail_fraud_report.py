import mysql.connector
import pandas as pd
from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
import os
import sys

# =========================
# CONFIG
# =========================
OUTPUT_PATH = r"C:\Users\klaus\Documents\Perfil Profesional\GitHub\Proyecto_2\Output\retail_fraud_report.pdf"

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "nirvana92",
    "database": "sales"
}

# =========================
# CONEXIÓN
# =========================
try:
    conn = mysql.connector.connect(**DB_CONFIG)
    print("✅ Conectado")
except Exception as e:
    print("❌ Error conexión:", e)
    sys.exit()

# =========================
# DATA
# =========================
query = """
SELECT 
    s.sale_id,
    s.customer_id,
    s.store_id,
    s.product_id,
    s.date,
    s.quantity,
    s.price,
    f.fraud_id
FROM sales s
LEFT JOIN fraud_flags f ON s.sale_id = f.sale_id
"""

df = pd.read_sql(query, conn)

# =========================
# LIMPIEZA
# =========================
df['date'] = pd.to_datetime(df['date'])
df['fraud'] = df['fraud_id'].notnull().astype(int)
df['total'] = df['quantity'] * df['price']

# CAST A ENTEROS
df['sale_id'] = df['sale_id'].astype('Int64')
df['customer_id'] = df['customer_id'].astype('Int64')
df['store_id'] = df['store_id'].astype('Int64')
df['product_id'] = df['product_id'].astype('Int64')

# =========================
# KPIs
# =========================
ventas_totales = int(df['total'].sum())
ticket_promedio = int(df['total'].mean())
clientes = df['customer_id'].nunique()
total_transacciones = df['sale_id'].nunique()
fraudes = int(df['fraud'].sum())
ratio_fraude = round(fraudes / total_transacciones, 3)

# =========================
# FRAUDE POR CLIENTE
# =========================
fraude_cliente = df.groupby('customer_id').agg({
    'fraud': 'sum',
    'sale_id': 'count',
    'total': 'sum'
}).reset_index()

fraude_cliente['ratio'] = (fraude_cliente['fraud'] / fraude_cliente['sale_id']).round(3)

fraude_cliente = fraude_cliente.sort_values(by='fraud', ascending=False).head(10)

# FORMATO
fraude_cliente['total'] = fraude_cliente['total'].astype(int)

# =========================
# VENTAS POR TIENDA
# =========================
ventas_tienda = df.groupby('store_id')['total'].sum().reset_index()
ventas_tienda['total'] = ventas_tienda['total'].astype(int)
ventas_tienda = ventas_tienda.sort_values(by='total', ascending=False).head(5)

# =========================
# VENTAS POR PRODUCTO
# =========================
ventas_producto = df.groupby('product_id')['total'].sum().reset_index()
ventas_producto['total'] = ventas_producto['total'].astype(int)
ventas_producto = ventas_producto.sort_values(by='total', ascending=False).head(5)

# =========================
# FUNCIÓN TABLA PRO
# =========================
def crear_tabla(data):
    tabla = Table(data)
    tabla.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.darkblue),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('ALIGN', (0,0), (-1,-1), 'CENTER')
    ]))
    return tabla

# =========================
# PDF
# =========================
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

doc = SimpleDocTemplate(OUTPUT_PATH, pagesize=letter)
styles = getSampleStyleSheet()

contenido = []

# TÍTULO
contenido.append(Paragraph("EXECUTIVE FRAUD & SALES REPORT", styles['Title']))
contenido.append(Spacer(1, 20))

# KPIs
contenido.append(Paragraph("Resumen Ejecutivo", styles['Heading2']))
contenido.append(Spacer(1, 10))

contenido.append(Paragraph(f"Ventas Totales: ${ventas_totales:,}", styles['Normal']))
contenido.append(Paragraph(f"Ticket Promedio: ${ticket_promedio:,}", styles['Normal']))
contenido.append(Paragraph(f"Clientes: {clientes}", styles['Normal']))
contenido.append(Paragraph(f"Transacciones: {total_transacciones}", styles['Normal']))
contenido.append(Paragraph(f"Fraudes detectados: {fraudes}", styles['Normal']))
contenido.append(Paragraph(f"Ratio de fraude: {ratio_fraude:.3f}", styles['Normal']))

contenido.append(Spacer(1, 25))

# FRAUDE
contenido.append(Paragraph("Top Clientes con Fraude", styles['Heading2']))
contenido.append(Spacer(1, 10))

tabla1 = [list(fraude_cliente.columns)] + fraude_cliente.values.tolist()
contenido.append(crear_tabla(tabla1))

contenido.append(Spacer(1, 25))

# TIENDAS
contenido.append(Paragraph("Ventas por Tienda", styles['Heading2']))
contenido.append(Spacer(1, 10))

tabla2 = [list(ventas_tienda.columns)] + ventas_tienda.values.tolist()
contenido.append(crear_tabla(tabla2))

contenido.append(Spacer(1, 25))

# PRODUCTOS
contenido.append(Paragraph("Ventas por Producto", styles['Heading2']))
contenido.append(Spacer(1, 10))

tabla3 = [list(ventas_producto.columns)] + ventas_producto.values.tolist()
contenido.append(crear_tabla(tabla3))

# BUILD
doc.build(contenido)

print("✅ REPORTE PERFECTO GENERADO")