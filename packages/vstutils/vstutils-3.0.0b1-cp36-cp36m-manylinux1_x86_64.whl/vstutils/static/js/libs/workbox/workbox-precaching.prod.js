this.workbox=this.workbox||{},this.workbox.precaching=function(t,e,n,s,c){"use strict";try{self["workbox:precaching:4.3.1"]&&_()}catch(t){}const o=[],i={get:()=>o,add(t){o.push(...t)}};const a="__WB_REVISION__";function r(t){if(!t)throw new c.WorkboxError("add-to-cache-list-unexpected-type",{entry:t});if("string"==typeof t){const e=new URL(t,location);return{cacheKey:e.href,url:e.href}}const{revision:e,url:n}=t;if(!n)throw new c.WorkboxError("add-to-cache-list-unexpected-type",{entry:t});if(!e){const t=new URL(n,location);return{cacheKey:t.href,url:t.href}}const s=new URL(n,location),o=new URL(n,location);return o.searchParams.set(a,e),{cacheKey:o.href,url:s.href}}class l{constructor(t){this.t=e.cacheNames.getPrecacheName(t),this.s=new Map}addToCacheList(t){for(const e of t){const{cacheKey:t,url:n}=r(e);if(this.s.has(n)&&this.s.get(n)!==t)throw new c.WorkboxError("add-to-cache-list-conflicting-entries",{firstEntry:this.s.get(n),secondEntry:t});this.s.set(n,t)}}async install({event:t,plugins:e}={}){const n=[],s=[],c=await caches.open(this.t),o=await c.keys(),i=new Set(o.map(t=>t.url));for(const t of this.s.values())i.has(t)?s.push(t):n.push(t);const a=n.map(n=>this.o({event:t,plugins:e,url:n}));return await Promise.all(a),{updatedURLs:n,notUpdatedURLs:s}}async activate(){const t=await caches.open(this.t),e=await t.keys(),n=new Set(this.s.values()),s=[];for(const c of e)n.has(c.url)||(await t.delete(c),s.push(c.url));return{deletedURLs:s}}async o({url:t,event:e,plugins:o}){const i=new Request(t,{credentials:"same-origin"});let a,r=await s.fetchWrapper.fetch({event:e,plugins:o,request:i});for(const t of o||[])"cacheWillUpdate"in t&&(a=t.cacheWillUpdate.bind(t));if(!(a?a({event:e,request:i,response:r}):r.status<400))throw new c.WorkboxError("bad-precaching-response",{url:t,status:r.status});r.redirected&&(r=await async function(t){const e=t.clone(),n="body"in e?Promise.resolve(e.body):e.blob(),s=await n;return new Response(s,{headers:e.headers,status:e.status,statusText:e.statusText})}(r)),await n.cacheWrapper.put({event:e,plugins:o,request:i,response:r,cacheName:this.t,matchOptions:{ignoreSearch:!0}})}getURLsToCacheKeys(){return this.s}getCachedURLs(){return[...this.s.keys()]}getCacheKeyForURL(t){const e=new URL(t,location);return this.s.get(e.href)}}let u;const h=()=>(u||(u=new l),u);const d=(t,e)=>{const n=h().getURLsToCacheKeys();for(const s of function*(t,{ignoreURLParametersMatching:e,directoryIndex:n,cleanURLs:s,urlManipulation:c}={}){const o=new URL(t,location);o.hash="",yield o.href;const i=function(t,e){for(const n of[...t.searchParams.keys()])e.some(t=>t.test(n))&&t.searchParams.delete(n);return t}(o,e);if(yield i.href,n&&i.pathname.endsWith("/")){const t=new URL(i);t.pathname+=n,yield t.href}if(s){const t=new URL(i);t.pathname+=".html",yield t.href}if(c){const t=c({url:o});for(const e of t)yield e.href}}(t,e)){const t=n.get(s);if(t)return t}};let w=!1;const f=t=>{w||((({ignoreURLParametersMatching:t=[/^utm_/],directoryIndex:n="index.html",cleanURLs:s=!0,urlManipulation:c=null}={})=>{const o=e.cacheNames.getPrecacheName();addEventListener("fetch",e=>{const i=d(e.request.url,{cleanURLs:s,directoryIndex:n,ignoreURLParametersMatching:t,urlManipulation:c});if(!i)return;let a=caches.open(o).then(t=>t.match(i)).then(t=>t||fetch(i));e.respondWith(a)})})(t),w=!0)},y=t=>{const e=h(),n=i.get();t.waitUntil(e.install({event:t,plugins:n}).catch(t=>{throw t}))},p=t=>{const e=h(),n=i.get();t.waitUntil(e.activate({event:t,plugins:n}))},L=t=>{h().addToCacheList(t),t.length>0&&(addEventListener("install",y),addEventListener("activate",p))};return t.addPlugins=(t=>{i.add(t)}),t.addRoute=f,t.cleanupOutdatedCaches=(()=>{addEventListener("activate",t=>{const n=e.cacheNames.getPrecacheName();t.waitUntil((async(t,e="-precache-")=>{const n=(await caches.keys()).filter(n=>n.includes(e)&&n.includes(self.registration.scope)&&n!==t);return await Promise.all(n.map(t=>caches.delete(t))),n})(n).then(t=>{}))})}),t.getCacheKeyForURL=(t=>{return h().getCacheKeyForURL(t)}),t.precache=L,t.precacheAndRoute=((t,e)=>{L(t),f(e)}),t.PrecacheController=l,t}({},workbox.core._private,workbox.core._private,workbox.core._private,workbox.core._private);