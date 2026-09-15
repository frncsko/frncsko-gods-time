st.markdown("---")
        st.markdown("### 📋 Citas Registradas")
        if st.session_state.citas_db:
            st.dataframe(pd.DataFrame(st.session_state.citas_db), use_container_width=True)

    # 5. ADMINISTRACIÓN (RESTRICCIÓN DE PERMISOS)
    with tab_admin:
        st.markdown("### ⚙️ Panel de Control del Administrador")
        
        if es_admin:
            st.warning("⚠️ **Atención:** La siguiente opción borrará permanentemente las citas y cortes.")
            if st.button("🔴 REINICIAR TODO EL HISTORIAL"):
                st.session_state.cortes_db = []
                st.session_state.citas_db = []
                guardar_datos(CORTES_FILE, [])
                guardar_datos(CITAS_FILE, [])
                st.success("El historial completo ha sido borrado.")
                st.rerun()
        else:
            st.error("🔒 **Acceso restringido:** Tu usuario (Jonder) no posee permisos para borrar o reiniciar el historial de la barbería.")
