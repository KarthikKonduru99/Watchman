"use strict";(self["webpackChunkaw_webui"]=self["webpackChunkaw_webui"]||[]).push([[5953],{25953:(t,n,r)=>{r.r(n),r.d(n,{default:()=>f});var e=function(){var t=this,n=t._self._c;return n("div",{attrs:{id:"forcegraph"}})},o=[],i=r(90537),a=(r(41539),r(47042),r(74916),r(23123),r(21249),r(69600),r(56604));const u={name:"ForceGraph",props:{data:{type:Object,required:!0}},data:function(){return{cancelPromise:null}},watch:{data:function(){this.drawGraph(this.data)}},mounted:function(){this.drawGraph(this.data)},methods:{drawGraph:function(t){var n=this,r=t.nodes,e=t.links;console.log("rendering..."),this.cancelPromise&&this.cancelPromise();var o=new Promise((function(t){n.cancelPromise=t})),i=c({nodes:r,links:e},{invalidation:o}),u=a.select("#forcegraph");u.selectAll("*").remove(),u.node().appendChild(i),console.log("drawn!")}}};function c(t){var n=t.nodes,r=t.links,e=arguments.length>1&&void 0!==arguments[1]?arguments[1]:{},o=e.nodeId,u=void 0===o?function(t){return t.id}:o,c=e.nodeGroup,l=void 0===c?function(t){return t.group}:c,d=e.nodeGroups,s=e.nodeTitle,f=void 0===s?function(t){return t.id.split(">").slice(-1)}:s,v=e.nodeFill,p=void 0===v?"currentColor":v,h=e.nodeStroke,k=void 0===h?"#fff":h,g=e.nodeStrokeWidth,m=void 0===g?1.5:g,y=e.nodeStrokeOpacity,x=void 0===y?1:y,w=e.nodeRadius,b=void 0===w?4:w,j=e.nodeStrength,S=e.linkSource,C=void 0===S?function(t){var n=t.source;return n}:S,G=e.linkTarget,O=void 0===G?function(t){var n=t.target;return n}:G,P=e.linkStroke,T=void 0===P?"#999":P,q=e.linkStrokeOpacity,M=void 0===q?.6:q,_=e.linkStrokeWidth,A=void 0===_?function(t){return 1.5*Math.sqrt(t.value)}:_,B=e.linkStrokeLinecap,F=void 0===B?"round":B,L=e.linkStrength,W=void 0===L?function(t){return t.value<10?.01:Math.sqrt(1/(2+t.value))}:L,Z=e.colors,I=void 0===Z?a.schemeTableau10:Z,R=e.width,z=void 0===R?640:R,D=e.height,E=void 0===D?400:D,H=e.invalidation,J=a.map(n,u).map(it),K=a.map(r,C).map(it),N=a.map(r,O).map(it);void 0===f&&(f=function(t,n){return J[n]});var Q=null==f?null:a.map(n,f),U=null==l?null:a.map(n,l).map(it),V="function"!==typeof A?null:a.map(r,A),X="function"!==typeof T?null:a.map(r,T);n=a.map(n,(function(t,n){return{id:J[n],color:t.color,value:t.value}})),r=a.map(r,(function(t,n){return{source:K[n],target:N[n],value:t.value}})),n=n.map((function(t){return t.radius=b+5*Math.sqrt(t.value/60/60),t})),U&&void 0===d&&(d=a.sort(U));var Y=null==l?null:a.scaleOrdinal(d,I),$=a.forceManyBody(),tt=a.forceLink(r).id((function(t){var n=t.index;return J[n]}));void 0!==j&&$.strength(j),void 0!==W&&tt.strength(W);var nt=a.forceSimulation(n).force("link",tt).force("charge",$).force("center",a.forceCenter()).force("collision",a.forceCollide((function(t){return t.radius}))).on("tick",at),rt=a.create("svg").attr("width",z).attr("height",E).attr("viewBox",[-z/2,-E/2,z,E]).attr("style","max-width: 100%; height: auto; height: intrinsic;"),et=rt.append("g").attr("stroke","function"!==typeof T?T:null).attr("stroke-opacity",M).attr("stroke-width","function"!==typeof A?A:null).attr("stroke-linecap",F).selectAll("line").data(r).join("line"),ot=rt.append("g").attr("fill",p).attr("stroke",k).attr("stroke-opacity",x).attr("stroke-width",m).selectAll("circle").data(n).join("circle").attr("r",(function(t){return t.radius})).call(ut(nt));function it(t){return null!==t&&"object"===(0,i.Z)(t)?t.valueOf():t}function at(){et.attr("x1",(function(t){return t.source.x})).attr("y1",(function(t){return t.source.y})).attr("x2",(function(t){return t.target.x})).attr("y2",(function(t){return t.target.y})),ot.attr("cx",(function(t){return t.x})).attr("cy",(function(t){return t.y}))}function ut(t){function n(n){n.active||t.alphaTarget(.3).restart(),n.subject.fx=n.subject.x,n.subject.fy=n.subject.y}function r(t){t.subject.fx=t.x,t.subject.fy=t.y}function e(n){n.active||t.alphaTarget(0),n.subject.fx=null,n.subject.fy=null}return a.drag().on("start",n).on("drag",r).on("end",e)}return V&&et.attr("stroke-width",(function(t){var n=t.index;return V[n]})),X&&et.attr("stroke",(function(t){var n=t.index;return X[n]})),ot.attr("fill",(function(t){var r=t.index;return n[r].color})),Q&&ot.append("title").text((function(t){var n=t.index;return Q[n]})),null!=H&&H.then((function(){return nt.stop()})),Object.assign(rt.node(),{scales:{color:Y}})}const l=u;var d=r(1001),s=(0,d.Z)(l,e,o,!1,null,null,null);const f=s.exports}}]);
//# sourceMappingURL=5953.d51591b7.js.map