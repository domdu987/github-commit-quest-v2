import sys; sys.path.insert(0, sys.argv[1]); import desert as D
for loc, pr in (('desert_ice', 'channels_wide'), ('desert_ice', 'dome_interior'), ('bazaar', 'bazaar_wide')):
    A = D.build(loc, pr); print(pr, A['marks']); print('  lights', len(A['lights']), A['lights'])
    print('  digest', D.digest())
