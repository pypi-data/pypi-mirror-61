!function(){"use strict";function e(e,t,n){for(var a,o=function(e){for(var t="",n=0;n<e.childNodes.length;n++){var a=e.childNodes[n];if("code"===a.tagName.toLowerCase())for(var o=0;o<a.childNodes.length;o++){var i=a.childNodes[o];if("#text"===i.nodeName&&!/^\s*$/.test(i.nodeValue)){t=i.nodeValue;break}}}return t},i=document.querySelectorAll("article"),r=document.querySelectorAll("pre.".concat(t,",div.").concat(t)),d=void 0===n?{}:n,c=0;c<r.length;c++){var l=r[c],s=document.createElement("div");s.className=t,s.style.visibility="hidden",s.style.position="absolute";var u="pre"===l.tagName.toLowerCase()?o(l):(a=l).textContent||a.innerText;i[0].appendChild(s),e.parse(u).drawSVG(s,d),s.style.visibility="visible",s.style.position="static",l.parentNode.insertBefore(s,l),l.parentNode.removeChild(l)}}var t;t=function(){"undefined"!=typeof flowchart&&e(flowchart,"uml-flowchart"),"undefined"!=typeof Diagram&&e(Diagram,"uml-sequence-diagram",{theme:"simple"})},document.addEventListener?document.addEventListener("DOMContentLoaded",t):document.attachEvent("onreadystatechange",function(){"interactive"===document.readyState&&t()})}();