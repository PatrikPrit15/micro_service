# start up for windows

1. dostat sa do dir micro_service
2. pip install requirements.txt najlepsie do venv
3. python otvorit python v cmd
4. from micro_service import db
5. db.create_all()
6. exit()
7. set FLASK_APP=micro_service.py
8. set FLASK_ENV=development
9. flask run alebo python -m flask run na mojom notebooku prve neslo


# endpoints

  ## users
  1. /users/post/<userId>/ GET
     vrati vsetky posty od uzivatela s id userId

  ## posts
  1. /posts/<post_id>/ GET
     vrati post s id post_id
  2. /posts/ POST
     data su: userId, title, body
     vytvori novy post a prida do db
  3. /posts/<post_id>/ PUT
     data su: title, body
     zmeni prispevok na post_id na novy v db
  4. /posts/<post_id>/ DELETE
     vymaze prispevok z db
