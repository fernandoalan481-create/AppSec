"""Report generation: JSON and TXT outputs."""
import json
from datetime import datetime
from pathlib import Path
from core.ui import strip_ansi
from config.settings import DATA_DIR

def salvar_relatorio(relatorio: dict, base_name: str):
    """Save report as JSON and TXT."""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_json = DATA_DIR / f"{base_name}_{timestamp}.json"
    output_txt = DATA_DIR / f"{base_name}_{timestamp}.txt"
    
    try:
        # Clean report for JSON (strip ANSI)
        clean_relatorio = {
            k: strip_ansi(str(v)) if isinstance(v, str) else v 
            for k, v in relatorio.items() 
            if k != 'secao'
        }
        if 'secao' in relatorio:
            clean_relatorio['secao'] = [
                {
                    'titulo': s.get('titulo'),
                    'conteudo': strip_ansi(str(s.get('conteudo', '')))
                }
                for s in relatorio['secao']
            ]
        
        with open(output_json, "w", encoding="utf-8") as f:
            json.dump(clean_relatorio, f, indent=2, ensure_ascii=False)
        
        # TXT version (no colors, structured)
        with open(output_txt, "w", encoding="utf-8") as f:
            if 'cabecalho' in relatorio:
                f.write(strip_ansi(relatorio['cabecalho']))
            if 'secao' in relatorio:
                for secao in relatorio['secao']:
                    f.write(f"\n\n{secao.get('titulo', '')}\n")
                    f.write(strip_ansi(str(secao.get('conteudo', ''))))
        
        print(f"[✓] Reports saved:")
        print(f"  📄 {output_txt.name}")
        print(f"  📊 {output_json.name}")
    except Exception as e:
        print(f"[!] Report save error: {e}")

