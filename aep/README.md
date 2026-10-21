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

## Privacidad de las credenciales

El fichero de credenciales contiene el client secret de la integración OAuth de Adobe Developer Console. Con él se pueden pedir tokens y actuar en la organización de AEP con todos los permisos de la integración, así que el paquete está escrito para que el secreto no salga del equipo salvo hacia Adobe IMS.

### Ubicación del fichero

El fichero se guarda solo en el equipo de quien ejecuta el paquete, en la raíz del repositorio. El `.gitignore` excluye `*.postman_environment.json`, de modo que no entra en ningún commit ni se sube a GitHub. El nombre del fichero puede cambiar siempre que conserve esa terminación, porque es la que usa `aep/` para encontrarlo y la que cubren el `.gitignore` y las reglas de Claude Code que se describen más abajo.

### Datos que salen del equipo

| Valor | Destino | Uso |
| --- | --- | --- |
| `CLIENT_ID` y `CLIENT_SECRET` | Adobe IMS (`https://{IMS}/ims/token/v3`), en el cuerpo de una petición POST | Obtener el token de acceso |
| Token de acceso | `platform.adobe.io`, en la cabecera `Authorization` | Llamar a las APIs REST y obtener los parámetros de conexión de Query Service |
| Token de acceso | El servidor PostgreSQL de Query Service, como contraseña de la conexión | Lanzar SQL |
| `API_KEY`, `IMS_ORG` y `SANDBOX_NAME` | `platform.adobe.io`, en las cabeceras `x-api-key`, `x-gw-ims-org-id` y `x-sandbox-name` | Identificar la integración, la organización y la sandbox |

Todas las conexiones van cifradas: las llamadas por HTTPS y la conexión a Query Service con `sslmode=require`.

El client secret se envía al host de IMS que indique la variable `IMS` del fichero, o a `ims-na1.adobelogin.com` si no la tiene. El fichero tiene que ser, por tanto, el que se descarga de Adobe Developer Console, sin modificar.

### Protecciones del paquete

1. No imprime ni registra en ningún log los valores del fichero ni el token. El código no usa `print` ni `logging`.
2. No escribe el token en disco. Lo guarda en memoria mientras dura el proceso, lo da por caducado un minuto antes de que caduque y entonces pide otro.
3. Al imprimir la configuración, por ejemplo con `print(load_config())`, `AEPConfig` no muestra `client_id`, `client_secret`, `api_key` ni `org_id`, porque esos campos están fuera de su `repr`.
4. Los mensajes de error no incluyen los valores del fichero ni el token. Indican qué ha fallado con la ruta del fichero, el nombre de la variable que falta, la URL y el código de la respuesta y, en las APIs de Platform, el cuerpo de la respuesta de error.

### Límites

1. Dejar los campos fuera del `repr` solo protege al imprimir el objeto entero. `config.client_secret`, `dataclasses.asdict(config)` o `vars(config)` devuelven los valores, así que ningún script debe imprimir ni guardar esos atributos.
2. El fichero está en claro en el disco. Su protección depende de los permisos del equipo y de no copiarlo a otras carpetas, unidades compartidas, correos ni mensajes.
3. Cualquier script que importe el paquete puede leer el fichero sin nombrarlo, porque `aep/` lo localiza por su terminación.

### Uso con un asistente de IA

El paquete se ha desarrollado con Claude Code, que ejecuta scripts que usan `aep/` sin ver el contenido del fichero de credenciales. En el equipo de desarrollo se aplican tres medidas:

1. Reglas de denegación en la configuración de usuario de Claude Code (`~/.claude/settings.json`), que le impiden abrir el fichero con sus herramientas de lectura y búsqueda:

   ```json
   "permissions": {
     "deny": [
       "Read(**/*.postman_environment.json)",
       "Read(//**/*.postman_environment.json)"
     ]
   }
   ```

2. Un hook `PreToolUse` en la misma configuración, que deniega cualquier comando de PowerShell o Bash cuyo texto contenga `postman_env`. Así tampoco puede leer el fichero desde el shell.
3. La revisión por una persona de cada script que use `aep/` antes de ejecutarlo, porque un script puede abrir el fichero sin nombrarlo y ni las reglas ni el hook lo detectarían. Claude Code solo ve los resultados y los errores de las llamadas.

Estas medidas están en la configuración de usuario de Claude Code y no en el repositorio. Quien use el paquete con Claude Code o con otro asistente tiene que configurar las suyas antes de dejar el fichero en la raíz.

### Exposición del secreto

Si el client secret aparece en un commit, un log, una captura o una conversación con un asistente, hay que generar uno nuevo en el proyecto de Adobe Developer Console, borrar el anterior y descargar de nuevo el fichero de credenciales. Borrar el commit o el mensaje no basta, porque el valor puede estar ya copiado en otro sitio.

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
