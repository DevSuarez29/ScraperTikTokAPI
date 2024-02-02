from flask import Flask, render_template, request
import pandas as pd
import urllib.parse
from ScraperTikTokAPI import ScraperTikTokAPI

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def scrape():
    tiktok_url = request.form.get('tiktok_url', '')  # Use get to avoid KeyError
    resultados = ScraperTikTokAPI.Comment.comments(tiktok_url)
    df = pd.DataFrame(resultados)
    all_reply = [] 
    df_filtrado = df[df['reply_comment_total'] > 0]
    cid_array = df_filtrado['cid'].unique()
    for cid_valor in cid_array:
        resultados_reply = ScraperTikTokAPI.Comment.reply(cid_valor)
        all_reply.extend(resultados_reply)

    df_reply_comment = pd.DataFrame(all_reply)
    video_id = urllib.parse.urlparse(tiktok_url).path.split('/')[-1]
    nombre_archivo_excel = f"static/datos_{video_id}.xlsx"
    with pd.ExcelWriter(nombre_archivo_excel, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Comment', index=False)
        df_reply_comment.to_excel(writer, sheet_name='Reply', index=False)

    return render_template('result.html', data=df.to_html(), filename=nombre_archivo_excel)

if __name__ == '__main__':
    app.run(debug=True)

