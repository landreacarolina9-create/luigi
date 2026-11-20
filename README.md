# Luigi · Asistente de Menú con IA

Prototipo académico de recomendación de platos para Luigi · Buffet Italiano. Aplicación web Streamlit conectada a Google Gemini.

## Publicación gratuita en Streamlit Community Cloud

1. En GitHub, crea un repositorio nuevo llamado `luigi-menu-ia`. Puede ser **público**; nunca subas claves al repositorio.
2. Entra al repositorio, pulsa **Add file → Upload files** y sube **los cuatro archivos de la raíz** de este paquete: `app.py`, `engine.py`, `menu.csv`, `requirements.txt` (también puedes subir `README.md`). No subas el ZIP sin extraer.
3. En https://share.streamlit.io inicia sesión con GitHub, selecciona **Create app**, el repositorio, rama `main` y archivo principal `app.py`.
4. Antes de desplegar, abre **Advanced settings → Secrets** e introduce (con TU clave real):

```toml
GEMINI_API_KEY = "TU_CLAVE_PRIVADA"
GEMINI_MODEL = "gemini-2.5-flash"
```

5. Pulsa **Deploy**. Al finalizar, Streamlit mostrará el enlace público `https://...streamlit.app`. Comparte ese enlace con el profesor.

Si ya desplegaste sin clave, entra a **Manage app → Settings → Secrets** para añadirla y reinicia la app.

## Advertencias
- No pegues la clave en `app.py`, GitHub, capturas ni mensajes. Si una clave se filtra, revócala en Google AI Studio.
- Gemini tiene límites gratuitos; la disponibilidad del modelo depende de tu cuenta y región.
- Los precios y la disponibilidad de `menu.csv` son de ejemplo y deben validarse con el restaurante antes de usarse como datos reales.
- La latencia de Gemini puede superar los 5 segundos. Registra tiempos reales en las pruebas, no los inventes.
- Streamlit Community Cloud puede suspender aplicaciones inactivas; el primer acceso posterior puede tardar.

## Pruebas recomendadas
1. Mucha hambre, sin afán, antojo queso.
2. Hambre normal, con afán, sin antojo.
3. Hambre normal, sin afán, vegetariano.
4. Hambre normal, con afán, antojo ambiguo.
5. Campos vacíos: mostrar aviso sin consultar IA.
6. Alergias: remitir al personal.
7. Confirmar que nunca se sugieran platos marcados como no disponibles.

## Ejecución local (opcional)
`python -m pip install -r requirements.txt` y `python -m streamlit run app.py`. La clave se obtiene desde secretos de Streamlit o variable de entorno `GEMINI_API_KEY`.
