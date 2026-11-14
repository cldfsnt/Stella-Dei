from PIL import Image,ImageDraw
from pathlib import Path
import numpy as np
from scipy.ndimage import distance_transform_edt
root=Path(__file__).resolve().parent
names=['mat','cushion','rosette','ribbon','branching','canopy']
atlas=Image.new('RGBA',(576,384))
proof=Image.new('RGB',(768,340),'#215f69');draw=ImageDraw.Draw(proof)
for i,name in enumerate(names):
 raw=Image.open(root/'renders'/f'{name}.png').convert('RGBA');crop=raw.crop(raw.getchannel('A').getbbox());ratio=172/max(crop.size);crop=crop.resize((round(crop.width*ratio),round(crop.height*ratio)),Image.Resampling.LANCZOS);im=Image.new('RGBA',(192,192));im.paste(crop,((192-crop.width)//2,182-crop.height));arr=np.array(im);alpha=arr[:,:,3].copy();distance,nearest=distance_transform_edt(alpha==0,return_indices=True);bleed=(alpha==0)&(distance<=4);arr[bleed,:3]=arr[nearest[0][bleed],nearest[1][bleed],:3];assert np.array_equal(alpha,arr[:,:,3]);im=Image.fromarray(arr);atlas.paste(im,((i%3)*192,(i//3)*192))
 proof.paste(im.resize((112,112),Image.Resampling.LANCZOS),(i*128+8,15),im.resize((112,112),Image.Resampling.LANCZOS))
 draw.text((i*128+8,137),name,fill='white')
 for y,sz in [(165,40),(225,32),(280,25)]:
  small=im.resize((sz,sz),Image.Resampling.LANCZOS);proof.paste(small,(i*128+40,y),small)
 draw.text((i*128+8,320),'40 / 32 / 25px',fill='#aaccbb')
atlas.save(root/'aquatic-forms-atlas.png');atlas.save(root.parents[1]/'assets/aquatic-forms-atlas.png');proof.save(root/'legibility-sheet.png')
