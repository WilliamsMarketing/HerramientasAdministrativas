import streamlit as st
import pandas as pd
import os

st.title("Calcula tu Rentabilidad Comercial📈")
st.write("---")

st.header("1. Ingresa tus números")
nombre_producto = st.text_input("Nombre del producto o campaña:")
precio_venta = st.number_input("Precio de venta al público (S/)", min_value=0.0)
costo_producto = st.number_input("Costo de producir o comprar (S/)", min_value=0.0)
costo_ads = st.number_input("Costo de publicidad en Meta Ads por venta (S/)", min_value=0.0)

# Cálculos
igv_calculado = precio_venta * 0.18
ingreso_sin_igv = precio_venta - igv_calculado
ganancia_neta = ingreso_sin_igv - costo_producto - costo_ads

st.header("2. Resultados Financieros")
st.write("IGV a reservar para Sunat (18%): S/", round(igv_calculado, 2))
st.write("Tu ingreso real (sin IGV): S/", round(ingreso_sin_igv, 2))
st.write("---")

st.header("3. Veredicto del Negocio")
if ganancia_neta > 0:
    st.success(f"¡Excelente! Tienes una ganancia neta de S/ {round(ganancia_neta, 2)} libres. Tu campaña es rentable.")
elif ganancia_neta == 0:
    st.warning("Punto de equilibrio. Pagaste el producto y la publicidad, pero tu ganancia es S/ 0.00.")
else:
    st.error(f"¡Alerta! Tienes una pérdida de S/ {round(ganancia_neta, 2)}. Necesitas optimizar tus anuncios en Meta o subir el precio.")

st.write("---")
st.header("4. Distribución del Dinero 📊")
tabla_datos = pd.DataFrame({
    "Conceptos": ["Costo del Producto", "Publicidad Meta Ads", "IGV Sunat", "Ganancia Neta"],
    "Soles (S/)": [costo_producto, costo_ads, igv_calculado, ganancia_neta]
})
st.bar_chart(tabla_datos, x="Conceptos", y="Soles (S/)")

st.write("---")
st.header("5. Historial de Productos")

# Botón para guardar en el sistema interno
if st.button("💾 Guardar cálculo internamente"):
    if nombre_producto == "":
        st.error("Por favor, escribe el nombre del producto arriba antes de guardar.")
    else:
    # Creamos una fila con el resumen de este producto (AHORA REDONDEADO)
        nuevo_registro = pd.DataFrame({
            "Producto": [nombre_producto],
            "Precio Venta": [round(precio_venta, 2)],
            "Costo": [round(costo_producto, 2)],
            "Meta Ads": [round(costo_ads, 2)],
            "Ganancia Neta": [round(ganancia_neta, 2)]
        })
        archivo_existe = os.path.isfile("registro_productos.csv")
        nuevo_registro.to_csv("registro_productos.csv", mode='a', header=not archivo_existe, index=False, sep=';', decimal=',')
        st.success(f"¡El producto '{nombre_producto}' ha sido guardado exitosamente!")

st.write("---")
# NUEVO: Verificamos si el archivo existe en la computadora
if os.path.isfile("registro_productos.csv"):
    st.write("¿Quieres llevarte tu base de datos? Descárgala aquí:")
    
    # Leemos el archivo y creamos el botón de descarga web
    with open("registro_productos.csv", "rb") as file:
        st.download_button(
            label="📥 Descargar mi base de datos (Excel/CSV)",
            data=file,
            file_name="historial_mi_empresa.csv",
            mime="text/csv"
        )