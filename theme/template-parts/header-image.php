<?php
$img_path    = wp_get_original_image_path( get_field( 'post_image', 'option' ) );
$type        = pathinfo( $img_path, PATHINFO_EXTENSION );
$data        = base64_encode( file_get_contents( $img_path ) );
$image_sizes = wp_get_attachment_image_src( get_field( 'post_image', 'option' ), 'full' );
?>
<img src="<?php echo 'data:image/' . $type . ';base64,' .  $data; ?>" width="<?php echo $image_sizes[1]; ?>" height="<?php echo $image_sizes[2]; ?>" class="post-img no-lazy-load" alt="" title="<?php echo get_the_title( get_field( 'post_image', 'option' ) ); ?>" />
