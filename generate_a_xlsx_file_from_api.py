import requests
from openpyxl import Workbook

# Función para autenticarse y obtener el token
def obtener_token(usuario, clave):
    url = "url/api/v2/autenticar"
    payload = {
        "usuario": usuario,
        "clave": clave
    }
    headers = {
        'Content-Type': 'application/json'
    }
    # Aquí desactivamos la verificación del certificado SSL
    response = requests.post(url, json=payload, headers=headers, verify=False)
    if response.status_code == 200:
        return response.json()["token"]
    else:
        print("Error en la autenticación:", response.text)
        return None

# Función para extraer los productos de una página y guardarlos en un archivo Excel
def extraer_productos(token):
    wb = Workbook()
    ws = wb.active
    ws.append([
        "Nombre", "Producto", "PRECIO_OFERTA", "PRECIO", "SKU_ALTERNO",
        "VENCIMIENTO", "Categoria Niv 1", "Categoria Niv 2", "Categoria Niv 3",
        "CODIGO_INTERNO", "MARCA", "DESCRIPCION", "INVENTARIO", "CODIGO_COMBO"
    ])
    
    totalPages = 15
    for pagina in range(1, min(totalPages + 1, 91)):  # Extrae las primeras 50 páginas
        url = "url/api/v2/products"
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        payload = {
            "page": str(pagina),
            "limit": "100",
            "fecha": "2022-01-01"
        }
        # Aquí desactivamos la verificación del certificado SSL
        response = requests.post(url, json=payload, headers=headers, verify=False)
        if response.status_code == 200:
            data = response.json()["datos"]["results"]
            for producto in data:
                # Mapeo de datos
                nombre = producto.get("PRODUCTO", "")
                producto_nombre = producto.get("PRODUCTO", "")
                precio_oferta = producto.get("PRECIO_OFERTA", "")
                precio = producto.get("PRECIO", "")
                sku_alterno = producto.get("SKU_ALTERNO", "")
                vencimiento = producto.get("VENCIMIENTO", "")
                categoria_niv_1 = producto.get("CATEGORIA_NIV_1", "")
                categoria_niv_2 = producto.get("CATEGORIA_NIV_2", "")
                categoria_niv_3 = producto.get("CATEGORIA_NIV_3", "")
                codigo_interno = producto.get("CODIGO_INTERNO", "")
                marca = producto.get("MARCA", "")
                descripcion = producto.get("DESCRIPCION", "")
                inventario = producto.get("INVENTARIO", "")
                codigo_combo = producto.get("CODIGO_COMBO", "")
                
                # Transformación de "Vitaminas Y Minerales"
                if categoria_niv_1 == "Vitaminas Y Minerales":
                    categoria_niv_1 = "Vitaminas y Minerales"
                
                ws.append([
                    nombre, producto_nombre, precio_oferta, precio, sku_alterno,
                    vencimiento, categoria_niv_1, categoria_niv_2, categoria_niv_3,
                    codigo_interno, marca, descripcion, inventario, codigo_combo
                ])
            print(f"Productos de la página {pagina} extraídos y guardados en Excel.")
        else:
            print(f"Error al extraer productos de la página {pagina}:", response.text)
    
    wb.save("productos.xlsx")

# Parámetros de autenticación
usuario = "usuario"
clave = "clave"

# Autenticación y obtención del token
token = obtener_token(usuario, clave)
if token:
    # Extracción de todos los productos
    extraer_productos(token)
else:
    print("No se pudo obtener el token de autenticación.")
