from flask import Flask, render_template, request
import os
import markdown
import frontmatter
from pathlib import Path

app = Flask(__name__)
RECETAS_DIR = 'recetas'

# Función para cargar y procesar recetas
def cargar_recetas(directorio="recetas"):
    recetas = []
    path = Path(directorio)
    
    for archivo in path.glob("*.md"):
        with open(archivo, 'r', encoding='utf-8') as f:
            post = frontmatter.load(f)  # Ahora SÍ detecta el frontmatter
        
        receta = {
            'filename': archivo.stem,
            'title': post.metadata.get('Title', 'Sin título'),
            'date': post.metadata.get('Date', '1970-01-01'),
            'category': post.metadata.get('Category', 'Sin categoría'),
            'tags': post.metadata.get('Tags', '').split(', '),
            'content': post.content.strip(),  # Todo el Markdown sin frontmatter
            'image': None
        }
        
        # Extraer imagen si existe en el contenido
        if '![Tarta]' in receta['content'] or '![Gazpacho]' in receta['content']:
            import re
            match = re.search(r'!\[.*?\]\((images/.*?)\)', receta['content'])
            if match:
                receta['image'] = match.group(1)
        
        recetas.append(receta)
    
    # Ordenar por fecha descendente
    recetas.sort(key=lambda x: x['date'], reverse=True)
    return recetas

# Página principal con lista de recetas y buscador
@app.route('/', methods=['GET', 'POST'])
def index():
    recetas = cargar_recetas()
    termino_busqueda = request.form.get('search', '').lower() if request.method == 'POST' else ''
    
    # Filtrar recetas si hay término de búsqueda
    if termino_busqueda:
        recetas = [
            receta for receta in recetas
            if termino_busqueda in receta['title'].lower() or
               termino_busqueda in receta['content'].lower() or
               any(termino_busqueda in tag.lower() for tag in receta['tags'])
        ]
    
    return render_template('index.html', recetas=recetas, termino_busqueda=termino_busqueda)

# Página individual de receta
@app.route('/receta/<nombre>')
def receta(nombre):
    try:
        with open(os.path.join(RECETAS_DIR, nombre+'.md'), 'r', encoding='utf-8') as f:
            post = frontmatter.load(f)
            html = markdown.markdown(post.content, extensions=['extra'])
            return render_template('receta.html', html=html, title=post.get('title', nombre))
    except FileNotFoundError:
        return "Receta no encontrada", 404

def test_ficheros_recetas():
    recetas = cargar_recetas()
    for r in recetas:
        print(f"{r['title']} | {r['category']} | {', '.join(r['tags'])}")

if __name__ == '__main__':
    test_ficheros_recetas()
    app.run(debug=True)