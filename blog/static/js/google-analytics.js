// Google tag(gtag.js)
function loadGoogleAnalytics() {
  var ga = document.createElement('script');
  ga.type = 'text/javascript';
  ga.async = true;
  ga.src = 'https://www.googletagmanager.com/gtag/js?id=G-113XQ18ZQ6';

  var s = document.getElementsByTagName('script')[0];
  s.parentNode.insertBefore(ga, s);
}

loadGoogleAnalytics(); //Create the script  

window.dataLayer = window.dataLayer || [];
function gtag() { dataLayer.push(arguments); }
gtag('js', new Date());

gtag('config', 'G-113XQ18ZQ6');