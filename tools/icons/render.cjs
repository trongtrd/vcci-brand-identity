const fs=require('fs'),path=require('path');
const sharp=require('sharp');
const root=path.resolve(__dirname,'..'), catalog=JSON.parse(fs.readFileSync(path.join(__dirname,'catalog.json'),'utf8'));
async function main(){
 let jobs=[];
 for(const i of catalog){
  for(const [variant,file] of Object.entries(i.paths)){
   if(variant==='currentColor')continue;
   const svg=fs.readFileSync(file); const tier=i.tier;
   for(const size of tier==='UI'?[48,96]:[256,512]){
    const dest=file.replace(`${path.sep}SVG${path.sep}`,`${path.sep}PNG${path.sep}`).replace('.svg',`_${size}px.png`);
    fs.mkdirSync(path.dirname(dest),{recursive:true});jobs.push(()=>sharp(svg).resize(size,size).png().toFile(dest));
   }
   for(const size of [24,48,128]){
    for(const [bg,hex] of [['Paper','#FBF9F4'],['Blue','#264896']]){
     const dest=path.join(__dirname,'qa','renders',tier,variant,bg,`${i.slug}_${size}.png`);
     fs.mkdirSync(path.dirname(dest),{recursive:true});jobs.push(()=>sharp(svg).resize(size,size).flatten({background:hex}).png().toFile(dest));
    }
   }
   const dest=path.join(__dirname,'qa','alpha',tier,`${variant}_${i.slug}.png`);
   fs.mkdirSync(path.dirname(dest),{recursive:true});jobs.push(()=>sharp(svg).resize(tier==='UI'?480:640).png().toFile(dest));
  }
 }
 for(let j=0;j<jobs.length;j+=12)await Promise.all(jobs.slice(j,j+12).map(f=>f()));
 console.log(`Rendered ${jobs.length} exports and QA images.`);
}
main().catch(e=>{console.error(e);process.exit(1)});
