(this.webpackJsonp=this.webpackJsonp||[]).push([[5],{1124:function(e,t,n){"use strict";n.r(t);var r,c=n(0),i=n(921),u=n(115),l=n(83);!function(e){e.Added="added",e.Title="title",e.URL="original_url"}(r||(r={}));var a=n(851),o=Object(a.a)((function(){return{sortByOptions:Object(c.useMemo)((function(){return[{value:r.Added,label:"Date Added"},{value:r.Title,label:"Title"},{value:r.URL,label:"URL"}]}),[]),addEntryProps:Object(c.useMemo)((function(){return[{label:"Entry Title",name:"title"},{label:"Entry URL",name:"originalUrl"}]}),[]),api:{list:{useGet:function(){return Object(u.b)("/entry_list")},useAdd:function(){return Object(u.b)("/entry_list",l.a.Post)},useRemove:function(e){return Object(u.b)("/entry_list/".concat(e),l.a.Delete)}},entry:{useGet:function(e,t){return Object(u.b)("/entry_list/".concat(e,"/entries?").concat(t))},useAdd:function(e){return Object(u.b)("/entry_list/".concat(e,"/entries"),l.a.Post)},useRemove:function(e,t){return Object(u.b)("/entry_list/".concat(e,"/entries/").concat(t),l.a.Delete)},useRemoveBulk:function(e){return Object(u.b)("/entry_list/".concat(e,"/entries/batch"),l.a.Delete)}}}}})),s=n(7);t.default=function(){return Object(s.e)(o.Provider,null,Object(s.e)(i.a,{title:"Entry List"}))}}}]);
//# sourceMappingURL=EntryListPlugin.342000bdd5c02dfd0a9d.js.map