class App{constructor(api_config,openapi,cache){this.api=new ApiConnector(api_config,openapi,cache);this.error_handler=new ErrorHandler();this.languages=null;this.translations=null;this.user=null;}
start(){let LANG=guiLocalSettings.get('lang')||'en';let promises=[this.api.getLanguages(),this.api.getTranslations(LANG),this.api.loadUser(),];return Promise.all(promises).then(response=>{this.languages=response[0];this.translations={[LANG]:response[1],};this.user=response[2];fieldsRegistrator.registerAllFieldsComponents();this.mountApplication();}).catch(error=>{debugger;throw new Error(error);});}
mountApplication(){tabSignal.emit('app.beforeInit',{app:this});function setOriginalLinks(menu,host){for(let index=0;index<menu.length;index++){let item=menu[index];if(item.url){item.origin_link=true;item.url=host+'/#'+item.url;}
if(item.sublinks){item.sublinks=setOriginalLinks(item.sublinks,host);}}
return menu;}
let i18n=new VueI18n({locale:guiLocalSettings.get('lang')||'en',messages:this.translations,});let x_menu=setOriginalLinks([...app.api.openapi.info['x-menu']],this.api.getHostUrl());this.top_nav=new Vue({data:{a_links:true,},i18n:i18n,}).$mount('#top_nav_wrapper');this.sidebar=new Vue({data:{info:app.api.openapi.info,x_menu:x_menu,x_docs:app.api.openapi.info['x-docs'],a_links:true,},i18n:i18n,}).$mount('#sidebar_wrapper');this.gui_customizer=new Vue({i18n:i18n}).$mount('#gui_customizer_wrapper');this.footer=new Vue({i18n:i18n}).$mount('#main_footer_wrapper');tabSignal.emit('app.afterInit',{app:this});}}