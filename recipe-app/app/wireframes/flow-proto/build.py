import json
s=open('template.html').read()
s=s.replace('__SOUND__',open('sound.js').read()).replace('__DATA__',json.dumps(json.load(open('recipes.json')),ensure_ascii=False))
open('supper-flow-proto.html','w').write(s)
