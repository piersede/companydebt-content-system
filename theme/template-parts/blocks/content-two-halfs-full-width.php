<?php
$left_bg = get_field('two_halfs_full_width')['left_half']['colors']['background_color'];
$right_bg = get_field('two_halfs_full_width')['right_half']['colors']['background_color'];
$left_text_color = get_field('two_halfs_full_width')['left_half']['colors']['text_color'] ;
$supertitle_color = get_field('two_halfs_full_width')['section_heading']['colors']['supertitle_color'];
$title_color = get_field('two_halfs_full_width')['section_heading']['colors']['title_color'];
if ( empty( $left_text_color ) ) { $left_text_color = '#002856;'; }
$right_text_color = get_field('two_halfs_full_width')['right_half']['colors']['text_color'];
if ( empty( $right_text_color ) ) { $right_text_color = '#002856;'; }
?>

<?php if( have_rows('two_halfs_full_width') ): ?>
	<?php while( have_rows('two_halfs_full_width') ): the_row(); ?>


		<section class="section-two-halfs-full-width <?php if ( get_sub_field( 'add_classes' ) ) { the_sub_field( 'add_classes' );
		} ?>" style="background: linear-gradient(to right,<?php echo $left_bg; ?> 50%, <?php echo $right_bg; ?> 50%)">
			<div class="container">
                <div class="row">
                    <div class="col-12">
	                    <?php if( have_rows('section_heading') ): ?>
		                    <?php while( have_rows('section_heading') ): the_row(); ?>
			                    <?php if ( get_sub_field ('supertitle')) { ?>
                                    <div class="section-supertitle" style="color: <?php echo $supertitle_color; ?>"><?php the_sub_field( 'supertitle' ); ?></div>
			                    <?php } ?>
			                    <?php if ( get_sub_field ('title')) { ?>
                                    <h3 class="section-title" style="color: <?php echo $title_color; ?>"><?php the_sub_field( 'title' ); ?></h3>
			                    <?php } ?>
			                    <?php if ( get_sub_field ('description')) { ?>
                                    <div class="description" style="color: <?php echo $title_color; ?>"><?php the_sub_field( 'description' ); ?></div>
			                    <?php } ?>
		                    <?php endwhile;
	                    endif ?>
                    </div>
                </div>
				<div class="row">
		<?php if( have_rows('left_half') ): ?>
			<?php while( have_rows('left_half') ): the_row(); ?>
					<div class="col-6" style="color: <?php echo $left_text_color; ?>">
						<div class="content">
							<?php the_sub_field( 'wyswyg' ); ?>
						</div>
					</div>
			<?php endwhile;
		endif ?>
					<?php if( have_rows('right_half') ): ?>
						<?php while( have_rows('right_half') ): the_row(); ?>
                            <div class="col-6" style="color: <?php echo $right_text_color; ?>">
                                <div class="content">
									<?php the_sub_field( 'wyswyg' ); ?>
                                </div>
                            </div>
						<?php endwhile;
					endif ?>
				</div>
			</div>
		</section>
	<?php endwhile;
endif ?>