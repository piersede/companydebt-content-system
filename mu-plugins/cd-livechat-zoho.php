<?php
/* Plugin Name: CD LiveChat + Gravity Forms -> Zoho (widget + gclid capture + lead sync) */
if (!defined('ABSPATH')) exit;
if (!defined('CD_ZOHO_CLIENT_ID')) { $__s = __DIR__.'/cd-livechat-secrets.php'; if (file_exists($__s)) require_once $__s; }

add_action('wp_head', function(){
  /* Click-id capture, gated on advertising consent (added 29 Jul 2026).
   *
   * Previously this block stored gclid/gbraid/wbraid for 90 days straight off the
   * URL with NO consent check at all, and handed them to LiveChat as session
   * variables. That ran for every visitor - including anyone who pressed
   * "Reject All" - and the stored cookie was then read server-side and written
   * into the Zoho lead as Google_Click_ID (see the gform_after_submission
   * handler below). The banner said one thing and the code did another.
   *
   * Now: nothing is stored or forwarded unless the CookieYes cookie says
   * advertisement:yes. If consent is absent we actively DELETE any click-id
   * cookies already on the device - important, because the old 90-day cookies
   * do not expire just because the setter was fixed.
   *
   * Deliberate trade-off: if a visitor accepts only after navigating away from
   * the landing page, the click id is gone from the URL and is not recovered.
   * Stashing it "just in case" would be the same storage problem wearing a
   * different hat, so we accept the loss.
   */
  $js = <<<'CDLCJS'
(function () {
  var K = ['gclid', 'gbraid', 'wbraid'];
  function raw(n) {
    var m = document.cookie.match('(?:^|; )' + n + '=([^;]*)');
    return m ? decodeURIComponent(m[1]) : '';
  }
  /* Keyed on the advertisement category specifically - not "any of three
     categories", which is what the theme's cd-attribution.js still does. */
  function adConsent() {
    return /advertisement:yes/.test(raw('cookieyes-consent'));
  }
  function drop(k) {
    document.cookie = k + '=;path=/;max-age=0';
    document.cookie = k + '=;path=/;domain=' + location.hostname + ';max-age=0';
  }
  function store() {
    var p = new URLSearchParams(location.search);
    K.forEach(function (k) {
      var v = p.get(k);
      if (v) document.cookie = k + '=' + encodeURIComponent(v) + ';path=/;max-age=' +
        (90 * 86400) + ';SameSite=Lax' + (location.protocol === 'https:' ? ';Secure' : '');
    });
  }
  function collect() {
    var o = {};
    K.forEach(function (k) { var v = raw(k); if (v) o[k] = v; });
    o.landing_page = location.href;
    /* Explicit flag so the server-side chat webhook, which cannot see the
       visitor's cookies, knows this data arrived with consent behind it. */
    o.ad_consent = 'yes';
    return o;
  }
  function toLiveChat() {
    var vars = collect();
    window.__lc = window.__lc || {};
    window.__lc.params = window.__lc.params || [];
    Object.keys(vars).forEach(function (k) {
      window.__lc.params.push({ name: k, value: vars[k] });
    });
    function setSV() {
      try {
        if (window.LiveChatWidget && LiveChatWidget.call)
          LiveChatWidget.call('set_session_variables', vars);
      } catch (e) {}
    }
    if (window.LiveChatWidget) setSV();
    var t = setInterval(function () {
      if (window.LiveChatWidget) { setSV(); clearInterval(t); }
    }, 500);
    setTimeout(function () { clearInterval(t); }, 15000);
  }
  function run() {
    if (!adConsent()) { K.forEach(drop); return; }
    store();
    toLiveChat();
  }
  run();
  /* Re-run the moment consent is given, so a visitor who accepts while still on
     the landing page is captured properly. */
  document.addEventListener('cookieyes_consent_update', run);
})();
CDLCJS;
  echo '<script data-cd-lc="1">'.$js.'</script>'."\n";
  echo '<script data-cd-lc-embed="1">'.base64_decode('d2luZG93Ll9fbGMgPSB3aW5kb3cuX19sYyB8fCB7fTsKd2luZG93Ll9fbGMubGljZW5zZSA9IDgzMjEyMTE7CjsoZnVuY3Rpb24obix0LGMpe2Z1bmN0aW9uIGkobil7cmV0dXJuIGUuX2g/ZS5faC5hcHBseShudWxsLG4pOmUuX3EucHVzaChuKX12YXIgZT17X3E6W10sX2g6bnVsbCxfdjoiMi4wIixvbjpmdW5jdGlvbigpe2koWyJvbiIsYy5jYWxsKGFyZ3VtZW50cyldKX0sb25jZTpmdW5jdGlvbigpe2koWyJvbmNlIixjLmNhbGwoYXJndW1lbnRzKV0pfSxvZmY6ZnVuY3Rpb24oKXtpKFsib2ZmIixjLmNhbGwoYXJndW1lbnRzKV0pfSxnZXQ6ZnVuY3Rpb24oKXtpZighZS5faCl0aHJvdyBuZXcgRXJyb3IoIltMaXZlQ2hhdFdpZGdldF0gWW91IGNhbid0IHVzZSBnZXR0ZXJzIGJlZm9yZSBsb2FkLiIpO3JldHVybiBpKFsiZ2V0IixjLmNhbGwoYXJndW1lbnRzKV0pfSxjYWxsOmZ1bmN0aW9uKCl7aShbImNhbGwiLGMuY2FsbChhcmd1bWVudHMpXSl9LGluaXQ6ZnVuY3Rpb24oKXt2YXIgbj10LmNyZWF0ZUVsZW1lbnQoInNjcmlwdCIpO24uYXN5bmM9ITAsbi50eXBlPSJ0ZXh0L2phdmFzY3JpcHQiLG4uc3JjPSJodHRwczovL2Nkbi5saXZlY2hhdGluYy5jb20vdHJhY2tpbmcuanMiLHQuaGVhZC5hcHBlbmRDaGlsZChuKX19OyFuLl9fbGMuYXN5bmNJbml0JiZlLmluaXQoKSxuLkxpdmVDaGF0V2lkZ2V0PW4uTGl2ZUNoYXRXaWRnZXR8fGV9KHdpbmRvdyxkb2N1bWVudCxbXS5zbGljZSkp').'</script>'."\n";
}, 1);

add_action('rest_api_init', function () {
  register_rest_route('cd-livechat/v1','/hook',array('methods'=>'POST','callback'=>'cd_lc_hook','permission_callback'=>'__return_true'));
});
function cd_lc_log($m){ if (defined('CD_LC_DEBUG') && CD_LC_DEBUG) error_log('[CD-LC] '.(is_string($m)?$m:wp_json_encode($m))); }
function cd_lc_from_url($url,$key){ if(!$url||strpos($url,$key.'=')===false) return ''; $p=explode($key.'=',$url,2)[1]; return explode('&',$p,2)[0]; }

/* Has this visitor granted the advertising category? Reads the CookieYes cookie,
 * which is first-party and therefore present on the form POST. Returns false when
 * the cookie is missing, blank or malformed - i.e. absence of consent is treated
 * as refusal, never as permission. (Added 29 Jul 2026.) */
function cd_lc_ad_consent(){
  $c = isset($_COOKIE['cookieyes-consent']) ? (string) wp_unslash($_COOKIE['cookieyes-consent']) : '';
  return $c !== '' && strpos($c, 'advertisement:yes') !== false;
}

/* Strip click ids out of a URL before we store it. Without this the click id
 * still lands in Zoho via Website_URL even when Google_Click_ID is withheld. */
function cd_lc_strip_click_ids($url){
  if (!$url) return $url;
  $out = preg_replace('/([?&])(gclid|gbraid|wbraid|msclkid|fbclid)=[^&#]*/i', '$1', $url);
  $out = preg_replace('/[?&]+(#|$)/', '$1', $out);   // tidy a trailing ? or &
  return rtrim(preg_replace('/([?&])&+/', '$1', $out), '?&');
}
function cd_lc_names($name,$first,$last,$fallback){
  $first=trim((string)$first); $last=trim((string)$last); $name=trim((string)$name);
  if($first!=='' || $last!==''){ if($last===''){ $last=$first; $first=''; } return array($first,$last); }
  if($name==='') return array('',$fallback);
  $p=preg_split('/\s+/',$name,2);
  return count($p)<2 ? array('',$p[0]) : array($p[0],$p[1]);
}

// Fetch full chat by id from the LiveChat Agent API (read-only PAT, basic auth).
function cd_lc_get_chat($chat_id){
  if (!defined('CD_LC_ACCOUNT_ID') || !defined('CD_LC_PAT')) { cd_lc_log('no-pat'); return null; }
  $auth = base64_encode(CD_LC_ACCOUNT_ID.':'.CD_LC_PAT);
  $r = wp_remote_post('https://api.livechatinc.com/v3.5/agent/action/get_chat', array(
    'headers'=>array('Authorization'=>'Basic '.$auth,'Content-Type'=>'application/json'),
    'body'=>wp_json_encode(array('chat_id'=>$chat_id)), 'timeout'=>20));
  if (is_wp_error($r)) { cd_lc_log('getchat-wperr'); return null; }
  $b = wp_remote_retrieve_body($r); cd_lc_log('getchat '.substr($b,0,400));
  $j = json_decode($b,true); return is_array($j)?$j:null;
}

function cd_lc_hook(WP_REST_Request $req){
  if (!defined('CD_LC_SECRET') || $req->get_param('secret')!==CD_LC_SECRET) return new WP_REST_Response(array('ok'=>false,'err'=>'auth'),403);
  $body=$req->get_json_params(); cd_lc_log($body);
  // Workflow sends {"chat":"<chat_id>"}; also accept explicit chat_id or a full chat object.
  $chat_id=''; $chat=null;
  if (isset($body['chat']) && is_string($body['chat'])) $chat_id=$body['chat'];
  elseif (isset($body['chat_id']) && is_string($body['chat_id'])) $chat_id=$body['chat_id'];
  elseif (isset($body['chat']) && is_array($body['chat'])) $chat=$body['chat'];
  elseif (isset($body['payload']['chat']) && is_array($body['payload']['chat'])) $chat=$body['payload']['chat'];
  if ($chat_id && !$chat) $chat=cd_lc_get_chat($chat_id);

  $name=''; $email=''; $gclid=''; $gbraid=''; $url=''; $ad_consent='';
  if (is_array($chat)) foreach (($chat['users']??array()) as $u){
    if (($u['type']??'')!=='customer') continue;
    if (!$name)  $name=$u['name']??'';
    if (!$email) $email=$u['email']??'';
    foreach (($u['session_fields']??array()) as $sf){ if(is_array($sf)) foreach($sf as $k=>$v){
      if($k==='gclid'&&$v) $gclid=$v; elseif($k==='gbraid'&&$v) $gbraid=$v; elseif($k==='landing_page'&&$v) $url=$v;
      elseif($k==='ad_consent'&&$v) $ad_consent=$v; } }
    if (!$url && !empty($u['last_visit']['last_pages'][0]['url'])) $url=$u['last_visit']['last_pages'][0]['url'];
  }
  /* This is a server-to-server webhook from LiveChat, so there are no visitor
   * cookies to read. Consent is instead carried explicitly as the ad_consent
   * session variable, which the wp_head script only ever sets when the
   * advertisement category was granted. Anything without that flag is treated as
   * no consent: the URL fallback is skipped and click ids are dropped, because
   * landing_page carries ?gclid= and would otherwise reinstate them.
   * (Added 29 Jul 2026.) */
  if ($ad_consent === 'yes') {
    if(!$gclid && $url) $gclid=cd_lc_from_url($url,'gclid');
    if(!$gbraid && $url) $gbraid=cd_lc_from_url($url,'gbraid');
  } else {
    $gclid=''; $gbraid=''; $url=cd_lc_strip_click_ids($url);
  }

  list($cd_fn,$cd_ln)=cd_lc_names($name,'','','Live Chat visitor');
  $fields=array('Lead_Source'=>'Live Chat - CD','Last_Name'=>$cd_ln,'Email'=>$email,'Website_URL'=>$url);
  if($cd_fn!=='') $fields['First_Name']=$cd_fn;
  if($gclid) $fields['Google_Click_ID']=$gclid;
  if($gbraid) $fields['gbraid']=$gbraid;
  if($req->get_param('dry')) return new WP_REST_Response(array('ok'=>true,'dry'=>true,'chat_id'=>$chat_id,'parsed'=>$fields),200);
  $dbg = defined('CD_LC_DEBUG') && CD_LC_DEBUG;
  if(!$email && !$name){ if(!$dbg) return new WP_REST_Response(array('ok'=>true,'skip'=>'no-contact'),200);
    $fields['Last_Name']='LC DEBUG (no contact)'; $fields['Description']='chat_id='.$chat_id.' body='.substr(wp_json_encode($body),0,3000); }
  $t=cd_zoho_token(); if(!$t) return new WP_REST_Response(array('ok'=>false,'err'=>'token'),500);
  $ex=$email?cd_zoho_find_lead($t,$email):0; $res=cd_zoho_write($t,$ex,$fields);
  return new WP_REST_Response(array('ok'=>true,'chat_id'=>$chat_id,'updated'=>(bool)$ex,'parsed'=>$fields,'zoho'=>$res),200);
}
function cd_zoho_token(){ $c=get_transient('cd_zoho_access'); if($c) return $c;
  $r=wp_remote_post(CD_ZOHO_ACCOUNTS.'/oauth/v2/token',array('body'=>array('grant_type'=>'refresh_token','client_id'=>CD_ZOHO_CLIENT_ID,'client_secret'=>CD_ZOHO_CLIENT_SECRET,'refresh_token'=>CD_ZOHO_REFRESH_TOKEN)));
  if(is_wp_error($r)) return ''; $j=json_decode(wp_remote_retrieve_body($r),true);
  if(empty($j['access_token'])){ cd_lc_log($j); return ''; } set_transient('cd_zoho_access',$j['access_token'],3300); return $j['access_token']; }
function cd_zoho_find_lead($t,$email){ $r=wp_remote_get(CD_ZOHO_API.'/crm/v2/Leads/search?criteria='.rawurlencode('(Email:equals:'.$email.')'),array('headers'=>array('Authorization'=>'Zoho-oauthtoken '.$t)));
  if(is_wp_error($r)) return 0; $j=json_decode(wp_remote_retrieve_body($r),true); return $j['data'][0]['id']??0; }
function cd_zoho_write($t,$id,$fields){ $m=$id?'PUT':'POST'; if($id) $fields['id']=$id;
  $r=wp_remote_request(CD_ZOHO_API.'/crm/v2/Leads',array('method'=>$m,'headers'=>array('Authorization'=>'Zoho-oauthtoken '.$t,'Content-Type'=>'application/json'),'body'=>wp_json_encode(array('data'=>array($fields),'trigger'=>array()))));
  $b=is_wp_error($r)?'wperr':wp_remote_retrieve_body($r); cd_lc_log($b); $j=json_decode($b,true);
  $row=$j['data'][0]??array('raw'=>substr($b,0,120));
  if(($row['code']??'')!=='SUCCESS') error_log('[CD-LC] zoho-write-fail '.substr($b,0,300)); // always-on: never fail silently
  return $row; }

// Website forms -> Zoho. LABEL-aware extraction: CD's Gravity Forms mostly use plain
// text fields (labelled Name/Email/Phone), not GF's typed fields, so type-only matching
// missed most of them. Match by type OR label. Validated against all 9 live forms.
add_action('gform_after_submission', function($entry, $form){
  if (!function_exists('rgar')) return;
  $ftitle = isset($form['title']) ? (string)$form['title'] : '';
  if (stripos($ftitle,'feedback') !== false) return; // feedback form is not a lead

  $email=''; $name=''; $phone=''; $company=''; $first=''; $last=''; $message=''; $extras=array();
  if (!empty($form['fields'])) foreach ($form['fields'] as $f){
    $id=$f->id; $type=$f->type; $lbl=strtolower(rtrim(trim((string)$f->label),': '));
    if ($type==='name'){ if($name===''){ $n=trim(rgar($entry,$id.'.3').' '.rgar($entry,$id.'.6')); if($n==='') $n=trim((string)rgar($entry,(string)$id)); $name=$n; } continue; }
    $val=trim((string)rgar($entry,(string)$id));
    if ($company==='' && strpos($lbl,'company')!==false){ $company=$val; continue; }
    if ($email==='' && ($type==='email' || strpos($lbl,'email')!==false)){ if(strpos($val,'@')!==false) $email=$val; continue; }
    if ($phone==='' && ($type==='phone' || strpos($lbl,'phone')!==false || strpos($lbl,'telephone')!==false || strpos($lbl,'mobile')!==false)){ if($val!=='') $phone=$val; continue; }
    if ($first==='' && strpos($lbl,'first name')!==false){ $first=$val; continue; }
    if ($last==='' && strpos($lbl,'last name')!==false){ $last=$val; continue; }
    if ($name==='' && ($lbl==='name' || $lbl==='your name' || $lbl==='full name')){ $name=$val; continue; }
    if ($message==='' && ($type==='textarea' || strpos($lbl,'message')!==false || strpos($lbl,'comment')!==false)){ $message=$val; continue; }
    if ($val!=='' && (strpos($lbl,'amount')!==false || strpos($lbl,'guarantee')!==false)) $extras[]=trim((string)$f->label).': '.$val; // preserve debt figures
  }
  if ($name==='') $name=trim($first.' '.$last);
  if ($email==='' && $name==='') return;

  $url=rgar($entry,'source_url');
  /* Click ids only when the advertising category was granted. Both routes are
   * gated: the cookie (set by the wp_head script above, itself now consent-gated)
   * and the raw source_url, which carries ?gclid= straight from the landing page
   * and used to bypass the cookie entirely. When consent is absent we also strip
   * the ids out of the URL we store, or they simply arrive in Zoho by another
   * field. (Added 29 Jul 2026.) */
  $cd_ad_ok = cd_lc_ad_consent();
  if ($cd_ad_ok) {
    $gclid=cd_lc_from_url($url,'gclid'); if($gclid==='' && isset($_COOKIE['gclid'])) $gclid=$_COOKIE['gclid'];
    $gbraid=cd_lc_from_url($url,'gbraid'); if($gbraid==='' && isset($_COOKIE['gbraid'])) $gbraid=$_COOKIE['gbraid'];
  } else {
    $gclid=''; $gbraid=''; $url=cd_lc_strip_click_ids($url);
  }
  /* PPC landing pages. Without this every paid lead arrives as "Website Form - CD"
   * and is indistinguishable from an organic enquiry, which makes the ad spend
   * impossible to judge in the CRM. Detected two ways so a renamed form or a new
   * PPC URL still gets caught: the form id, or a /ppc- landing page in source_url.
   * The intent and the director's own description of their situation are the two
   * most useful qualifying details on the form, so they go into Description too. */
  $cd_ppc_form_ids = apply_filters('cd_zoho_ppc_form_ids', array(47));
  $cd_is_ppc = in_array((int)rgar($form,'id'), $cd_ppc_form_ids, true)
               || ($url && strpos($url,'/ppc-') !== false);

  $cd_intent=''; $cd_situation='';
  if ($cd_is_ppc && !empty($form['fields'])) foreach ($form['fields'] as $f){
    $lbl=strtolower(trim((string)$f->label));
    $val=trim((string)rgar($entry,(string)$f->id));
    if ($val==='') continue;
    if ($lbl==='intent') { $cd_intent=$val; continue; }
    if (strpos($lbl,'situation')!==false) {
      /* Store the choice TEXT, not the stored value ("cantpay"), so the CRM reads
       * as English. GF keeps both on the field. */
      $cd_situation=$val;
      if (!empty($f->choices)) foreach ($f->choices as $ch){
        if (isset($ch['value']) && (string)$ch['value']===$val && isset($ch['text'])) { $cd_situation=$ch['text']; break; }
      }
    }
  }

  $parts=array(); if($ftitle) $parts[]='['.$ftitle.']';
  if($cd_intent!=='') $parts[]='Ad intent: '.$cd_intent.'.';
  if($cd_situation!=='') $parts[]='Situation: '.$cd_situation.'.';
  if($message!=='') $parts[]=$message; if($extras) $parts[]=implode(' | ',$extras);
  $desc=trim(implode(' ',$parts));
  list($cd_fn,$cd_ln)=cd_lc_names($name,$first,$last,'Website enquiry');
  $cd_source = $cd_is_ppc ? 'PPC - CD' : 'Website Form - CD';
  $fields=array('Lead_Source'=>$cd_source,'Last_Name'=>$cd_ln,'Email'=>$email,'Mobile'=>$phone,'Website_URL'=>$url,'Description'=>$desc);
  if($cd_fn!=='') $fields['First_Name']=$cd_fn;
  if($company) $fields['Company']=$company;
  if($gclid) $fields['Google_Click_ID']=$gclid;
  if($gbraid) $fields['gbraid']=$gbraid;
  $t=cd_zoho_token(); if(!$t) return;
  $ex=$email?cd_zoho_find_lead($t,$email):0;
  cd_zoho_write($t,$ex,$fields);
}, 20, 2);
