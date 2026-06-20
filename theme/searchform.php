<?php
/**
 * The template for displaying the search form.
 *
 * @package Cd20
 */

?>
<style>
	#searchform {
		background: #e7f6fd;
		box-sizing: border-box;
		display: none;
		left: 0;
		position: absolute;
		right: 0;
		top: 0;
		transition: transform .3s;
		z-index: -2;
	}

</style>

<form role="search" id="search-form" class="search-form" method="get"
	  action="<?php echo esc_url( home_url( '/' ) ); ?>">


			<input itemprop="query-input" type="search" class="search-field" id="search-field" value="<?php echo get_search_query(); ?>"
				   placeholder="<?php echo esc_attr_x( 'Type search here &hellip;', 'placeholder', 'cd20' ); ?>"
				   name="s"/>
			<div class="search__button__container">
				<button type="submit" class="search-submit" value="">
					<img width="27" height="27" src="<?php echo CD_THEME_URL . 'assets/images/search-white.png'; ?>"
						 alt="search">
				</button>
			</div>


</form>
