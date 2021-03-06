from flask import Flask, send_file, request, render_template
import requests
from io import StringIO, BytesIO

app = Flask(__name__, static_folder='assets', static_url_path='/assets', template_folder='assets')


# http://54.160.74.94/groups/2526736/YLIMtolShWf0hRuvVcP2HFYa

@app.route('/')
def hello_world():
    return app.send_static_file('index.html')


@app.route('/bib')
def zotero_group():
    group_id = request.args.get('groupID')
    key = request.args.get('privateKey', default=None)
    print('Request', group_id, key)
    limit = 100
    start = limit
    base_url = 'https://api.zotero.org/groups/' + str(group_id) + \
               '/items/top?format=bibtex&style=numeric&limit=' + str(limit)
    if key:
        base_url += "&key=" + str(key)
    req = requests.get(base_url)
    req_text = req.text
    if req.ok is False:
        #     Error Handling
        return render_template('error.html', error_code=str(req.status_code), error_text=req_text)
    buffer = StringIO()
    buffer.write(req_text)
    # bib = req_text
    while req_text != '':
        request_url = base_url + "&start=" + str(start)
        print("Fetching ", request_url)
        req = requests.get(request_url)
        req_text = req.text
        buffer.write(req_text)
        start += limit

    # Convert String Buffer to BytesIO so that send_file works
    mem = BytesIO()
    mem.write(buffer.getvalue().encode())
    mem.seek(0)
    buffer.close()
    return send_file(mem, as_attachment=True,
                     attachment_filename='references.bib', mimetype='text/plain')

    # show the post with the given id, the id is an integer
    # return 'Post %d' % post_id


# https://api.zotero.org/groups/2579480/items/top?format=bibtex&style=numeric&limit=1000
# run the app.
# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    app.debug = True
    app.run()
