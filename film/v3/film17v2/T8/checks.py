import sys; sys.path.insert(0, "film/v3/set3d17"); import prefecture17 as P
r = P.check_take('T8'); print('check_take hits', r['hits'] if isinstance(r, dict) else r)
f = P.check_face('T8'); print('check_face ok', f['ok']); print(f['rows'])
