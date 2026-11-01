import json, sys, urllib.request, urllib.error, concurrent.futures as cf, os
LIB = {
 "field": ("Open dry grassland on a hot afternoon near a hill border: wind through tall grass, insects buzzing, distant birds, no music, no people", 8),
 "mine": ("A landmine explosion in an open grass field: a sharp deep boom, dirt and clods raining down, ringing aftermath, outdoors", 3),
 "tinnitus": ("High pitched ear ringing after an explosion, muffled world, slowly fading", 3),
 "debris": ("Clods of dirt and small stones raining down onto grass after a blast", 2),
 "whiz": ("Several rifle bullets whizzing past close overhead and snapping through leaves of a bush, distant gunshots", 3),
 "leaves": ("Leaves and twigs being shredded and snapping as bullets pass through a dense bush, close", 1.5),
 "distshots": ("Distant sporadic rifle gunfire echoing across hills, far away", 4),
 "crawl": ("A soldier crawling slowly through dry grass on his belly, fabric rustling, gear clinking softly", 2.5),
 "probe": ("A bayonet tip gently probing into dry soil, careful scraping, quiet breathing", 2),
 "truck": ("An old military truck engine idling and driving off on a dirt road", 3),
 "radio": ("Short military radio static burst with a click, no voice", 1),
 "dogtag": ("Metal dog tags on a ball chain jingling softly", 1),
 "songkran": ("Thai Songkran festival in a village street: water splashing, children laughing, distant festive music from a speaker, cheerful", 8),
 "parcel": ("A cardboard parcel being set down on a wooden step, then tape being torn open", 2),
 "rewind": ("A cassette tape rewinding fast, whirring with a click at the end", 1.2),
 "canvas": ("A heavy canvas-bound field notebook slapped down onto dry dirt, a soft thump and a little dust, close", 1.0),
 "pencil": ("A pencil sketching quickly on rough paper, scratchy strokes, close", 1.5),
 "buckle": ("A canvas strap swinging and its metal buckle clinking twice, close", 1.0),
 "spray": ("A spray paint can shaken with the ball rattling, then a short hiss of spray through a stencil", 1.5),
 "stake": ("A wooden stake knocked into dry ground with two thuds, then a rope creaking as a cardboard tag swings", 1.3),
}
def gen(k):
    text, d = LIB[k]
    out = f"{k}.mp3"
    if os.path.exists(out): return k, "cached"
    body = json.dumps({"text": text, "duration_seconds": max(0.5, d), "prompt_influence": 0.5}).encode()
    for a in range(3):
        try:
            req = urllib.request.Request("https://fal.run/fal-ai/elevenlabs/sound-effects/v2", data=body, headers={"Content-Type": "application/json"})
            r = json.load(urllib.request.urlopen(req, timeout=300))
            urllib.request.urlretrieve(r["audio"]["url"], out)
            return k, "ok"
        except Exception as e:
            err = str(e)
    return k, "fail " + err
with cf.ThreadPoolExecutor(5) as ex:
    for k, s in ex.map(gen, list(LIB)):
        print(k, s, flush=True)
