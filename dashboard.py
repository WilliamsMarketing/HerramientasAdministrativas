import streamlit as st
import pandas as pd

st.title("Simulador de Rentabilidad Comercial 📈")
st.write("---")

# 1. CREACIÓN DE LA PIZARRA MÁGICA (Memoria individual)
# Si el usuario es nuevo, le creamos un historial vacío en su sesión
if "historial" not in st.session_state:
    # Creamos una tabla de Pandas vacía con los títulos de las columnas
    st.session_state["historial"] = pd.DataFrame(columns=[
        "Producto", "Precio Venta", "Costo", "Meta Ads", "Ganancia Neta"
    ])

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
st.header("5. Historial de Productos (Privado)")

# 2. GUARDAR EN LA PIZARRA
if st.button("💾 Guardar cálculo en mi sesión"):
    if nombre_producto == "":
        st.error("Por favor, escribe el nombre del producto arriba antes de guardar.")
    else:
        # Creamos la fila con los datos redondeados
        nuevo_registro = pd.DataFrame({
            "Producto": [nombre_producto],
            "Precio Venta": [round(precio_venta, 2)],
            "Costo": [round(costo_producto, 2)],
            "Meta Ads": [round(costo_ads, 2)],
            "Ganancia Neta": [round(ganancia_neta, 2)]
        })
        
        # Pegamos la nueva fila a la tabla que está en la memoria del usuario usando pd.concat
        st.session_state["historial"] = pd.concat([st.session_state["historial"], nuevo_registro], ignore_index=True)
        
        st.success(f"¡El producto '{nombre_producto}' ha sido guardado temporalmente en tu sesión!")

st.write("---")

# 3. DESCARGAR DESDE LA PIZARRA
# Si la tabla en la memoria ya no está vacía (es decir, si ya guardó al menos un producto)
if not st.session_state["historial"].empty:
    st.write("Tus datos están listos y seguros. Descárgalos aquí:")
    
    # Convertimos la tabla de la memoria a formato CSV con punto y coma (para Excel en español)
    csv_seguro = st.session_state["historial"].to_csv(index=False, sep=';', decimal=',')
    
    # Creamos el botón de descarga
    st.download_button(
        label="📥 Descargar mi base de datos (Excel)",
        data=csv_seguro,
        file_name="reporte_privado_rentabilidad.csv",
        mime="text/csv"
    )