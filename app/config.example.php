<?php
return [
 'db'=>['host'=>'localhost','name'=>'schoolos','user'=>'schoolos_user','pass'=>'CHANGE_ME'],
 'app'=>[
  'name'=>'SchoolOS Nigeria','timezone'=>'Africa/Lagos',
  // Canonical HTTPS installation address; include a subdirectory when applicable.
  'cms_origin'=>'https://schoolos.example',
  // Add only school aliases already mapped in cPanel with a valid HTTPS certificate.
  'cms_allowed_hosts'=>[],
 ],
 'providers'=>['paystack_secret_key'=>'','whatsapp_token'=>'','sms_token'=>'','ai_api_key'=>''],
 // Optional server-managed per-school overrides. Otherwise use School Services → Providers.
 // Secret values belong only in the private config.php / encrypted settings, never in Git.
 'school_services'=>[],
];
