<?php
/**
 *
 * @package EpLight
 * @author  EmiPajk
 * @licence  GPL-2
 */
?>
<div class="bcg-image__full-width hero__bcg <?php echo $args['classes']; ?>">

	<div class="container">

		<picture class="hero__image">
			<img src="<?php echo $args['bcg_image'];?>">
		</picture>
		<div class="bcg-image__content  hero__content"
			 style="color:<?php echo $args['text_color']; ?>">
			<?php echo $args['wyswyg'] ?>
		</div>
	</div>
</div>


