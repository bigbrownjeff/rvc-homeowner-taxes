/* Shared header for all pages. Usage: <div id="site-nav" data-current="voices"></div>
   then <script src="assets/nav.js"></script> near the end of body (or defer). */
(function(){
  var mount=document.getElementById('site-nav'); if(!mount) return;
  var current=mount.getAttribute('data-current')||'';
  var privacyUrl='/privacy';
  var missionUrl='https://bluecamelconsulting.com/mission/?utm_source=rvc-housing-schools&utm_medium=referral&utm_campaign=civic-project';

  /* Top signup CTA is intentionally separate from the address-based action kit.
     It sends only email, explicit consent, and the page source to /api/signup. */
  var cta=document.createElement('div');
  cta.className='cta-strip'; cta.id='signup';
  cta.innerHTML=
    '<form class="cta-inner">'+
      '<div class="cta-copy">'+
        '<span class="cta-h">Get the 2027 senior-mobility and school-data update.</span>'+
        '<span id="signup-help" class="cta-sub">Email only. The address tool never subscribes you. Read the <a href="'+privacyUrl+'">privacy and unsubscribe policy</a>.</span>'+
      '</div>'+
      '<div class="cta-form">'+
        '<input type="email" name="email" class="cta-email" placeholder="you@email.com" aria-label="Your email address" aria-describedby="signup-help" autocomplete="email" maxlength="254" required>'+
        '<button type="submit" class="cta-btn">Sign up</button>'+
      '</div>'+
      '<label class="cta-consent"><input type="checkbox" name="consent" required> I agree to receive project updates. My email will not be added to a Blue Camel Consulting marketing list.</label>'+
      '<label class="cta-honeypot" aria-hidden="true">Leave this blank <input type="text" name="website" tabindex="-1" autocomplete="off"></label>'+
      '<div class="cta-msg" role="status" aria-live="polite"></div>'+
    '</form>';
  mount.parentNode.insertBefore(cta,mount);
  (function(){
    var form=cta.querySelector('form'),msg=cta.querySelector('.cta-msg'),
        btn=cta.querySelector('.cta-btn'),email=cta.querySelector('.cta-email'),
        consent=cta.querySelector('[name="consent"]'),honeypot=cta.querySelector('[name="website"]');
    function signupSource(){
      var source=new URLSearchParams(location.search).get('utm_source')||'';
      var allowed=['email','linkedin','bsky','threads','x','facebook'];
      return 'signup-strip:'+(allowed.indexOf(source)>=0?source:'direct');
    }
    function setMsg(t,cls){msg.textContent=t;msg.className='cta-msg show '+cls;}
    form.addEventListener('submit',function(e){
      e.preventDefault();
      if(!form.checkValidity()){form.reportValidity();return;}
      var v=email.value.trim();
      if(!v||v.indexOf('@')<1||v.indexOf('.')<0){setMsg('Enter a valid email address.','err');email.focus();return;}
      btn.disabled=true;var orig=btn.textContent;btn.textContent='Sending...';
      fetch('/api/signup',{method:'POST',headers:{'Content-Type':'application/json'},
        body:JSON.stringify({email:v,consent:consent.checked,website:honeypot.value,source:signupSource()})})
        .then(function(r){return r.ok?r.json():Promise.reject(r);})
        .then(function(){setMsg('You are on the list. Thank you.','ok');btn.textContent='Signed up';email.value='';email.disabled=true;consent.disabled=true;})
        .catch(function(){btn.disabled=false;btn.textContent=orig;setMsg('Something went wrong. Please try again.','err');});
    });
  })();
  var items=[
    {id:'brief',label:'The brief',href:'/'},
    {id:'mechanics',label:'Mechanics',href:'/fiscal-math'},
    {id:'factcheck',label:'Facts &amp; sources',href:'/validation'},
    {id:'voices',label:'Voices',href:'/voices'},
    {id:'calculator',label:'Calculator',href:'/calculator'}
  ];
  function links(cls){
    return items.map(function(it){
      return '<a href="'+it.href+'"'+(it.id===current?' class="current"':'')+'>'+it.label+'</a>';
    }).join('');
  }
  mount.className='site-nav';
  mount.innerHTML=
    '<div class="bar">'+
      '<a class="brand" href="/">RVC Housing &times; Schools</a>'+
      '<button class="menu-btn" aria-label="Menu" aria-expanded="false">Menu</button>'+
      '<div class="links">'+links()+'<a class="act" href="/#asks">Act now</a></div>'+
    '</div>'+
    '<div class="mobile">'+links()+'<a class="act" href="/#asks">Act now</a></div>';
  var btn=mount.querySelector('.menu-btn');
  btn.addEventListener('click',function(){
    var open=mount.classList.toggle('open');
    btn.textContent=open?'Close':'Menu';
    btn.setAttribute('aria-expanded',open?'true':'false');
  });
  document.querySelectorAll('.site-foot').forEach(function(footer){
    if(footer.querySelector('.independence-note')) return;
    var note=document.createElement('span');
    note.className='independence-note';
    note.innerHTML='Independent civic project by Jeff Pinto. <a href="'+missionUrl+'" target="_blank" rel="noopener">Blue Camel Consulting&rsquo;s mission-driven work</a>.';
    footer.appendChild(note);
  });
})();
