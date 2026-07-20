/* Shared header for all pages. Usage: <div id="site-nav" data-current="voices"></div>
   then <script src="assets/nav.js"></script> near the end of body (or defer). */
(function(){
  var mount=document.getElementById('site-nav'); if(!mount) return;
  var current=mount.getAttribute('data-current')||'';
  var items=[
    {id:'brief',label:'The brief',href:'index.html'},
    {id:'mechanics',label:'Mechanics',href:'fiscal-math.html'},
    {id:'factcheck',label:'Fact check',href:'validation.html'},
    {id:'voices',label:'Voices',href:'voices.html'},
    {id:'calculator',label:'Calculator',href:'calculator.html'}
  ];
  function links(cls){
    return items.map(function(it){
      return '<a href="'+it.href+'"'+(it.id===current?' class="current"':'')+'>'+it.label+'</a>';
    }).join('');
  }
  mount.className='site-nav';
  mount.innerHTML=
    '<div class="bar">'+
      '<a class="brand" href="index.html">RVC Housing &times; Schools</a>'+
      '<button class="menu-btn" aria-label="Menu" aria-expanded="false">Menu</button>'+
      '<div class="links">'+links()+'<a class="act" href="index.html#asks">Act now</a></div>'+
    '</div>'+
    '<div class="mobile">'+links()+'<a class="act" href="index.html#asks">Act now</a></div>';
  var btn=mount.querySelector('.menu-btn');
  btn.addEventListener('click',function(){
    var open=mount.classList.toggle('open');
    btn.textContent=open?'Close':'Menu';
    btn.setAttribute('aria-expanded',open?'true':'false');
  });
})();
