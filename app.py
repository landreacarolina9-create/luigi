import os
import time
import streamlit as st
from engine import read_menu, available_menu, check_special, ALLERGY_MESSAGE, gemini_recommendations

st.set_page_config(page_title="Luigi | Tu plato ideal", page_icon="🍝", layout="centered", initial_sidebar_state="collapsed")
st.markdown('''<style>
.stApp {background: #faf7f1; color:#26372e}
.block-container {max-width:850px;padding-top:2rem}
h1,h2,h3 {color:#23533b!important}
.stButton>button[kind="primary"] {background:#246845;border:0;border-radius:13px;color:white;font-weight:700;padding:0.8rem}
[data-testid="stForm"] {border:1px solid #e3e7dc;border-radius:18px;background:#fffdf8;padding:1.1rem}
[data-testid="stVerticalBlockBorderWrapper"] {border-radius:16px}
</style>''', unsafe_allow_html=True)

st.markdown('### 🍝 LUIGI · BUFFET ITALIANO')
st.title('¿Qué se te antoja hoy?')
st.write('Dinos cómo te sientes y nuestro asistente con inteligencia artificial te ayudará a elegir.')
st.caption('Prototipo académico · Cartagena, Colombia · Precios y disponibilidad sujetos a confirmación con el restaurante.')

try:
    df = read_menu('menu.csv')
except Exception:
    st.error('No se pudo cargar el menú. Contacta al administrador.')
    st.stop()

try:
    key = st.secrets.get('GEMINI_API_KEY', '')
    model = st.secrets.get('GEMINI_MODEL', 'gemini-2.5-flash')
except Exception:
    key = os.getenv('GEMINI_API_KEY', '')
    model = os.getenv('GEMINI_MODEL', 'gemini-2.5-flash')

with st.form('luigi_preferencias'):
    hambre = st.selectbox('🍽️ ¿Cuánta hambre tienes?', ['Selecciona una opción', 'Poca', 'Normal', 'Mucha'])
    tiempo = st.selectbox('⏱️ ¿Cuánto tiempo tienes?', ['Selecciona una opción', 'Voy con afán', 'Sin afán'])
    antojo = st.text_input('✨ ¿Qué se te antoja? (opcional)', placeholder='Por ejemplo: algo con queso, vegetariano o pasta', max_chars=160)
    enviar = st.form_submit_button('✨ Encuentra mi plato ideal', type='primary', use_container_width=True)

if enviar:
    if hambre == 'Selecciona una opción' and tiempo == 'Selecciona una opción' and not antojo.strip():
        st.warning('Cuéntanos al menos una preferencia para recomendarte un plato.')
    elif check_special(antojo) == 'alergia':
        st.warning(ALLERGY_MESSAGE)
    elif check_special(antojo) == 'sin_coincidencia':
        st.info('No encontramos una coincidencia segura con nuestra carta. Consulta los platos disponibles.')
    elif not key:
        st.error('El asistente de IA todavía no está configurado. El administrador debe añadir GEMINI_API_KEY en los secretos de Streamlit.')
    else:
        start = time.perf_counter()
        with st.spinner('Nuestro asistente está eligiendo tus platos...'):
            try:
                results = gemini_recommendations(df, hambre, tiempo == 'Voy con afán', antojo, key, model)
            except RuntimeError as exc:
                st.error(str(exc))
                results = None
            except Exception:
                st.error('No se pudo consultar la IA en este momento. Inténtalo nuevamente.')
                results = None
        if results is not None:
            if not results:
                st.info('No encontramos una recomendación segura con esas preferencias. Revisa la carta.')
            else:
                st.subheader('🍕 Recomendaciones para ti')
                for r in results:
                    with st.container(border=True):
                        st.markdown(f'#### {r["plato"]}')
                        price = format(r['precio_cop'], ',').replace(',', '.')
                        st.markdown(f'**{"Desde " if r["precio_desde"] else ""}${price} COP**')
                        st.write(r['razon'])
                        if r['sale_rapido']:
                            st.caption('⚡ Preparación rápida según el menú de ejemplo')
                st.caption(f'🤖 Generado con IA · {time.perf_counter()-start:.1f} s')

with st.expander('📋 Explorar el menú disponible'):
    view = available_menu(df)[['plato','categoria','precio_cop','precio_desde']].copy()
    view['precio_cop'] = view['precio_cop'].map(lambda x: ('$'+format(int(x),',').replace(',','.')+' COP') if x.isdigit() else 'Por confirmar')
    view.columns = ['Plato','Categoría','Precio','Desde']
    st.dataframe(view, hide_index=True, use_container_width=True)

st.divider()
st.caption('⚠️ Si tienes alergias o restricciones alimentarias, consulta al personal antes de ordenar. Luigi no procesa pagos ni pedidos. No ingreses información personal.')
