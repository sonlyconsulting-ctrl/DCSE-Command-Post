const fs=require('fs'),vm=require('vm'),assert=require('assert');
const root=process.argv[2]||require('path').resolve(__dirname,'..');
const catalog=JSON.parse(fs.readFileSync(root+'/content/escd-products-catalog.json','utf8'));
assert.equal(JSON.stringify(catalog),JSON.stringify(JSON.parse(fs.readFileSync(root+'/apps/escd/runtime/escd-products-catalog.json','utf8'))));
const html=fs.readFileSync(root+'/apps/escd/web/mvp.html','utf8');
for(const m of html.matchAll(/<script(?:\s[^>]*)?>([\s\S]*?)<\/script>/g))if(m[1].trim())new vm.Script(m[1]);
const fallback=html.slice(html.indexOf('const CANONICAL_PRODUCTS='),html.indexOf('let activeProdFilter='));
const render=html.slice(html.indexOf('function renderProductGrid('),html.indexOf('function filterCatalog('));
function el(tag,text,cls){return {tag,text,cls,style:{},children:[],append(...x){this.children.push(...x)},replaceChildren(){this.children=[]},setAttribute(k,v){this[k]=v}}}
const grid=el('div');const c=vm.createContext({el,$:()=>grid,loadedProducts:catalog.products});
vm.runInContext(render+';renderProductGrid();',c);
const expected={sc_enterprise:'https://sonlyconsulting.com',smoove_spots:'https://smoove-spots-c2a9eaaf-d58c-450d-a34.vercel.app'};
function check(products){assert.equal(grid.children.length,products.length);for(const [i,p] of products.entries()){const links=grid.children[i].children.flatMap(x=>x.children||[]).filter(x=>x.text==='🌐 Website ↗');assert.equal(links.length,expected[p.id]?1:0);for(const a of links){assert.equal(a.href,expected[p.id]);assert.equal(a.target,'_blank');assert.equal(a.rel,'noopener noreferrer');assert(a['aria-label'].includes(p.parent_brand));}const imgs=grid.children[i].children.flatMap(x=>x.children||[]).filter(x=>x.tag==='img');assert.equal(imgs.length,expected[p.id]?1:0);for(const img of imgs){assert.equal(img.src,p.actions.website_icon);assert.equal(img.alt,p.parent_brand+' website logo');assert.equal(img.style.objectFit,'contain');assert(img.width>0&&img.height>0);}}}
check(catalog.products);
vm.runInContext(fallback+';loadedProducts=CANONICAL_PRODUCTS;renderProductGrid();',c);check(vm.runInContext('CANONICAL_PRODUCTS',c));
console.log('PASS: both catalogs identical; scripts parse; API catalog and fallback each render exactly two correctly routed, accessible website links; other cards gain no website link.');
