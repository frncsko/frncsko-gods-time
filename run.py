import os
import sys
from streamlit.web import cli as stcli

def resolve_path(path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, path)
    return os.path.join(os.path.abspath("."), path)

if __name__ == "__main__":
    try:
        if hasattr(sys, '_MEIPASS'):
            os.chdir(sys._MEIPASS)
            
        app_path = resolve_path("app.py")
        
        os.sys.argv = [
            "streamlit",
            "run",
            app_path,
            "--server.headless=true",
            "--global.developmentMode=false",
        ]
        stcli.main()
    except Exception as e:
        import traceback
        traceback.print_exc()
        input("\n\nOcurrio un error. Presiona Enter para cerrar esta ventana...")