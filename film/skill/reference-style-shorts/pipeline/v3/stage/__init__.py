"""v3 staging system: puppets on cards in a Blender scene (see API.md).

    sys.path.insert(0, ".../v3");        from stage import actors, camrig, render, sprites, stubroom
or  sys.path.insert(0, ".../v3/stage");  import actors, camrig, render, sprites, stubroom

Use one of the two styles in a process, not both: each style creates its own module objects (camera key memory, actor
registry).  render.render_frames() syncs the actors of either style.  `sprites` needs no bpy.
"""
