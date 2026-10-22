<?php
// SchoolOS v2.7 image-upload handler. Loaded by the authenticated school setup router.
function ssUploadSchoolLogo($tenant,$upload){
 if(!isset($upload['error'])||$upload['error']===UPLOAD_ERR_NO_FILE)return null;
 if($upload['error']!==UPLOAD_ERR_OK||$upload['size']>2097152||$upload['size']<1)throw new RuntimeException('Logo must be an image under 2 MB.');
 if(!is_uploaded_file($upload['tmp_name']))throw new RuntimeException('Invalid upload.');
 $info=@getimagesize($upload['tmp_name']);$allowed=[IMAGETYPE_PNG=>'png',IMAGETYPE_JPEG=>'jpg',IMAGETYPE_WEBP=>'webp'];
 if(!$info||!isset($allowed[$info[2]])||$info[0]>4000||$info[1]>4000)throw new RuntimeException('Upload a valid PNG, JPG or WebP image (max 4000px).');
 $finfo=new finfo(FILEINFO_MIME_TYPE);$mime=$finfo->file($upload['tmp_name']);$expected=['png'=>'image/png','jpg'=>'image/jpeg','webp'=>'image/webp'];$ext=$allowed[$info[2]];
 if($mime!==$expected[$ext])throw new RuntimeException('Image type mismatch.');
 $root=__DIR__.'/uploads/schoolos-logos';if(!is_dir($root)&&!mkdir($root,0755,true))throw new RuntimeException('Upload directory unavailable.');if(!is_file($root.'/.htaccess'))throw new RuntimeException('Logo upload protection is missing. Install uploads/schoolos-logos/.htaccess first.');
 $file='school-'.(int)$tenant.'-'.bin2hex(random_bytes(12)).'.'.$ext;
 if(!move_uploaded_file($upload['tmp_name'],$root.'/'.$file))throw new RuntimeException('Could not save logo. Check upload permissions.');
 @chmod($root.'/'.$file,0644);
 return 'uploads/schoolos-logos/'.$file;
}
