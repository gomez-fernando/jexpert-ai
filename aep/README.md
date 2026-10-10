# aep

Paquete de Python para llamar a las APIs REST de Adobe Experience Platform y lanzar SQL en Query Service con unas credenciales OAuth server-to-server de Adobe Developer Console.

## Instalación

Con Python 3.10 o superior, desde la raíz del repositorio:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

`requirements.txt` instala las dependencias y el propio paquete en modo editable, así que `import aep` funciona desde cualquier carpeta con el entorno activo.

## Credenciales

El paquete lee el entorno de Postman que se descarga desde el proyecto de Adobe Developer Console (`*.postman_environment.json`). Basta con dejar ese fichero en la raíz del repositorio. Si hay más de uno, hay que indicar cuál con `credentials_path`.

El `.gitignore` excluye `*.postman_environment.json`, así que las credenciales no entran nunca en el repositorio.

Del fichero se usan estas variables:

| Variable | Uso |
| --- | --- |
| `CLIENT_ID` | Client ID de OAuth. Si falta, se usa `API_KEY`. |
| `CLIENT_SECRET` | Secreto de OAuth. |
| `API_KEY` | Cabecera `x-api-key`. Si falta, se usa `CLIENT_ID`. |
| `IMS_ORG` | Cabecera `x-gw-ims-org-id`. |
| `SANDBOX_NAME` | Sandbox por defecto, que se puede cambiar en cada llamada con `sandbox`. |
| `SCOPES` | Scopes que se piden a IMS. |
| `IMS` | Host de IMS. Por defecto, `ims-na1.adobelogin.com`. |

Postman puede guardar `SCOPES` como lista. IMS espera los scopes separados por comas y, si se le envían como parámetro repetido, solo concede el primero. En ese caso todas las llamadas a Platform responden 403 con el código `403027` ("User region is missing"). El paquete los une por comas antes de pedir el token.

## Query Service

```python
from aep import query_all, query_df, scalar

rows = query_all("select 1 as ok")
tables = query_df("show tables")
total = scalar("select count(*) from mi_tabla where timestamp >= %s", sql_params=["2026-10-01"])
```

| Función | Devuelve |
| --- | --- |
| `query_all` | Lista de diccionarios, uno por fila. |
| `query_df` | DataFrame de pandas. |
| `query_iter` | Generador de filas, para resultados grandes. |
| `scalar` | El primer valor de la primera fila. |
| `execute` | Nada. Para sentencias sin resultado. |

Todas aceptan `sql_params`, `credentials_path`, `sandbox`, `connect_timeout` y `query_timeout` (en segundos, 300 por defecto). Las consultas largas necesitan un `query_timeout` mayor. `query_all`, `query_df`, `scalar` y `execute` reintentan hasta tres veces, y solo ante errores transitorios. `query_iter` no reintenta, porque es un generador.

## APIs REST

```python
from aep import aep_get, aep_request

datasets = aep_get("/data/foundation/catalog/dataSets", params={"limit": 10, "properties": "name"})

schemas = aep_get(
    "/data/foundation/schemaregistry/tenant/schemas",
    headers={"Accept": "application/vnd.adobe.xed-id+json"},
)
```

`aep_get` devuelve el JSON de la respuesta. `aep_request(method, path, ...)` sirve para cualquier otro verbo y devuelve el `requests.Response` completo. `path` puede ser relativo a `https://platform.adobe.io` o una URL completa, como los enlaces de paginación que devuelven algunos servicios. La paginación no está incluida, porque cada servicio de Adobe pagina de una forma distinta.

## Errores

Todas las excepciones heredan de `AEPError`:

| Excepción | Causa |
| --- | --- |
| `AEPConfigError` | Falta el fichero de credenciales o alguna de sus variables. |
| `AEPAuthError` | IMS no devuelve el token. |
| `AEPConnectionError` | No se obtienen los parámetros de conexión de Query Service o falla la conexión PostgreSQL. |
| `AEPQueryError` | Falla la ejecución del SQL. |
| `AEPAPIError` | La API responde con un error o no responde. |
