def aplication(environ, start_response):
    respuesta = '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Document</title></head><body><p>Pagina web generada con Python</p></body></html>';
    start_response('200 OK',[('Content-Type', 'text/html; charset=utf-8')]);
    return [respuesta.encode()]
if __name__ == '__main__':
    pass;